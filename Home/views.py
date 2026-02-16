from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Prompt, Contact
from django.db.models import Q
from django.http import Http404

# Create your views here.
def home(request):
    query = request.GET.get('q', '').strip()  # get search query from ?q=
    
    model_tag_slug = request.GET.get("model")
    # Fetch only active prompts, latest first
    prompts_list = Prompt.objects.filter(is_private=False, is_verified=True, is_active=True) \
                            .only('id', 'title', 'image', 'created_at', 'user__username') \
                            .order_by('-created_at') \
                            .select_related("user")
                            
    if 2 < len(query) < 50:
        prompts_list = prompts_list.filter(
            Q(title__icontains=query) |
            Q(prompt__icontains=query) 
             
        ).distinct()
    
     
        
    if model_tag_slug:
        prompts_list = prompts_list.filter(models_supported__slug=model_tag_slug)   
    # Paginate the prompts, 5 per page
    paginator = Paginator(prompts_list, 10)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    try:
        prompt_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        raise Http404("not found")
    
    return render(request, 'index.html', {'prompt_obj': prompt_obj, 'query': query})


def singlePrompt(request, pk):
    # Fetch the prompt by ID
    prompt = get_object_or_404(Prompt.objects.prefetch_related('models_supported'), id=pk)
    
    if request.user.is_superuser:
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'verify':
                prompt.is_verified = True
                prompt.save()
                return redirect('admin-dashboard')
            elif action == 'delete':
                prompt.delete()
                return redirect('admin-dashboard')
    return render(request, 'single-prompt.html', {'prompt': prompt})

def comingSoon(request):
    return render(request, 'comingsoon.html')

  

def contactUs(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # Save the contact message to the database
        
        contact_message = Contact(
            name=name,
            email=email,
            message=message
        )
        contact_message.save()
        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')