from django.urls import path
from prompts import views
urlpatterns = [
    
    path('add/', views.addPrompt, name='add'),
    path('dashboard/', views.userDashboard, name='dashboard'),
    path('edit/<int:pk>', views.editPrompt, name='edit')
    
]