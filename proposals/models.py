from django.db import models
from django.contrib.postgres.fields import ArrayField


class Proposal(models.Model):
    # Input fields
    project_title = models.CharField(max_length=500)
    project_description = models.TextField()
    requirements = models.TextField()
    budget = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    client_name = models.CharField(max_length=200, blank=True)

    # Generated proposal
    generated_proposal = models.TextField()

    # Embedding for semantic search (stored as array of floats)
    embedding = ArrayField(
        models.FloatField(),
        size=384,  # Sentence transformer dimension
        null=True,
        blank=True
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_title} - {self.created_at.strftime('%Y-%m-%d')}"