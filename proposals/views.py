from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Proposal
from .ai_service import AIProposalService


def home(request):
    """Home page with proposal generation form"""
    return render(request, 'proposals/home.html')


def generate_proposal(request):
    """Handle proposal generation"""
    if request.method == 'POST':
        # Extract form data
        project_data = {
            'project_title': request.POST.get('project_title'),
            'project_description': request.POST.get('project_description'),
            'requirements': request.POST.get('requirements'),
            'budget': request.POST.get('budget', ''),
            'timeline': request.POST.get('timeline', ''),
            'client_name': request.POST.get('client_name', ''),
        }

        # Create proposal object
        proposal = Proposal(
            project_title=project_data['project_title'],
            project_description=project_data['project_description'],
            requirements=project_data['requirements'],
            budget=project_data['budget'],
            timeline=project_data['timeline'],
            client_name=project_data['client_name'],
        )

        # Generate proposal using AI
        ai_service = AIProposalService()
        generated_text = ai_service.generate_proposal(project_data)

        # Save with embedding
        ai_service.save_proposal_with_embedding(proposal, generated_text)

        messages.success(request, 'Proposal generated successfully!')
        return redirect('view_proposal', proposal_id=proposal.id)

    return redirect('home')


def view_proposal(request, proposal_id):
    """View a specific proposal"""
    proposal = get_object_or_404(Proposal, id=proposal_id)
    return render(request, 'proposals/view_proposal.html', {'proposal': proposal})


def proposal_history(request):
    """View all past proposals"""
    proposals = Proposal.objects.all()
    return render(request, 'proposals/history.html', {'proposals': proposals})


def delete_proposal(request, proposal_id):
    """Delete a proposal"""
    proposal = get_object_or_404(Proposal, id=proposal_id)
    proposal.delete()
    messages.success(request, 'Proposal deleted successfully!')
    return redirect('proposal_history')