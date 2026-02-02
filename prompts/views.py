from django.shortcuts import render

# Create your views here.

def userDashboard(request):
    return render(request, 'user-dashboard.html')

def addPrompt(request):
    return render(request, 'add-prompt.html')

