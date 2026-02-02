from django.urls import path
from Home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prompt/<int:pk>/', views.singlePrompt, name='prompt'),
    path('soon/', views.comingSoon, name='soon'),
    path('contact/', views.contactUs, name='contact'),

]