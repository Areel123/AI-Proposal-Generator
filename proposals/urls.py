from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_proposal, name='generate_proposal'),
    path('proposal/<int:proposal_id>/', views.view_proposal, name='view_proposal'),
    path('history/', views.proposal_history, name='proposal_history'),
    path('delete/<int:proposal_id>/', views.delete_proposal, name='delete_proposal'),
]