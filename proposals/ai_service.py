import os
import numpy as np
import faiss
from groq import Groq
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from .models import Proposal


class AIProposalService:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.proposal_ids = []
        self._build_index()

    def _build_index(self):
        """Build FAISS index from existing proposals"""
        proposals = Proposal.objects.exclude(embedding__isnull=True)

        if not proposals.exists():
            return

        embeddings = []
        self.proposal_ids = []

        for proposal in proposals:
            embeddings.append(np.array(proposal.embedding, dtype='float32'))
            self.proposal_ids.append(proposal.id)

        if embeddings:
            embeddings_array = np.array(embeddings)
            dimension = embeddings_array.shape[1]

            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings_array)

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using Sentence Transformer"""
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()

    def find_similar_proposals(self, query_embedding: List[float], k: int = 3) -> List[Proposal]:
        """Find k most similar proposals using FAISS"""
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = np.array([query_embedding], dtype='float32')
        k = min(k, self.index.ntotal)

        distances, indices = self.index.search(query_vector, k)

        similar_proposals = []
        for idx in indices[0]:
            if idx < len(self.proposal_ids):
                proposal_id = self.proposal_ids[idx]
                try:
                    proposal = Proposal.objects.get(id=proposal_id)
                    similar_proposals.append(proposal)
                except Proposal.DoesNotExist:
                    continue

        return similar_proposals

    def generate_proposal(self, project_data: Dict) -> str:
        """Generate proposal using Groq LLM with context from similar proposals"""

        # Create query text for similarity search
        query_text = f"{project_data['project_title']} {project_data['project_description']}"
        query_embedding = self.generate_embedding(query_text)

        # Find similar past proposals
        similar_proposals = self.find_similar_proposals(query_embedding, k=2)

        # Build context from similar proposals
        context = ""
        if similar_proposals:
            context = "\n\nHere are some similar past proposals for reference:\n"
            for i, prop in enumerate(similar_proposals, 1):
                context += f"\n--- Example {i} ---\n"
                context += f"Project: {prop.project_title}\n"
                context += f"Proposal excerpt: {prop.generated_proposal[:300]}...\n"

        # Build the prompt
        prompt = f"""You are a professional proposal writer. Generate a detailed, persuasive project proposal based on the following information:

Project Title: {project_data['project_title']}
Project Description: {project_data['project_description']}
Requirements: {project_data['requirements']}
Budget: {project_data.get('budget', 'To be discussed')}
Timeline: {project_data.get('timeline', 'Flexible')}
Client Name: {project_data.get('client_name', 'Valued Client')}
{context}

Generate a professional proposal with the following sections:
1. Executive Summary
2. Understanding of Requirements
3. Proposed Solution
4. Timeline and Milestones
5. Budget Breakdown
6. Why Choose Us
7. Next Steps

Make it persuasive, professional, and tailored to the specific project needs."""

        try:
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system",
                     "content": "You are an expert proposal writer with years of experience in creating winning project proposals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating proposal: {str(e)}"

    def save_proposal_with_embedding(self, proposal: Proposal, generated_text: str):
        """Save proposal with its embedding"""
        proposal.generated_proposal = generated_text

        # Generate and save embedding
        combined_text = f"{proposal.project_title} {proposal.project_description} {generated_text}"
        embedding = self.generate_embedding(combined_text)
        proposal.embedding = embedding

        proposal.save()

        # Rebuild index
        self._build_index()