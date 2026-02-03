from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Home.models import Prompt, AIModel
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.contrib.auth.models import User

# Create your views here.

@login_required
def userDashboard(request):
    prompts = Prompt.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(prompts, 9)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    try:
        prompt_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        raise Http404("not found")
    return render(request, 'user-dashboard.html', {"prompt_obj": prompt_obj, "prompts_count": prompts.count()})


@login_required
def addPrompt(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        prompt_text = request.POST.get('prompt')
        image = request.FILES.get('image')
        model_ids = request.POST.getlist("model_list")
        is_private = request.POST.get('is_private') == '1'

        # Create and save the new prompt
        if not (title or prompt_text or image or model_ids):
            messages.error(request, "No empty feilds")
            return redirect('add')
        
        
        new_prompt = Prompt.objects.create(
            title=title,
            prompt=prompt_text,
            image=image,
            user=request.user,
            is_private=is_private
        )
        if model_ids:
            new_prompt.models_supported.set(model_ids)
        return redirect('dashboard')
    return render(request, 'add-prompt.html', {'models': AIModel.objects.all()})

@login_required    
def editPrompt(request, pk):   #Edit and Delete both
    prompt = get_object_or_404(Prompt, user=request.user, id=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'save':
            is_private = request.POST.get('is_private') == '1'
            prompt.is_private = is_private
            prompt.save()
            return redirect('dashboard')
        elif action == 'delete':
            prompt.delete()
            return redirect('dashboard')
       
    
    return render(request, 'edit-prompt.html', {"prompt": prompt})

@login_required
def adminDashboard(request):
    if request.user.is_superuser:
        prompts = Prompt.objects.filter(is_verified=False).order_by('-created_at')
        paginator = Paginator(prompts, 9)
        page_number = request.GET.get('page')
        if page_number is None:
            page_number = 1
        try:
            prompt_obj = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            raise Http404("not found")
            
        
    else:
        return Http404("not found")
      
    
    return render(request, 'admin-dashboard.html', {"prompt_obj": prompt_obj, "prompts_count": prompts.count(), "total_users": User.objects.count()})


