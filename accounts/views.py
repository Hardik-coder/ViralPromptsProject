from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#xmna izoq ajhg hlyt
#token verification
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
#token verification

#Email template send
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
#Email template send

# Create your views here.
def signupUser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email", "").lower()
        username = request.POST.get("username")
        password = request.POST.get("password")
        

        # 1️ Email format check
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return redirect("signup")

        # 2️ Email uniqueness check
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered.")
            return redirect("signup")
        
        if len(username)>20:
            messages.error(request, "Username must be less than 15 characters")
            return redirect("signup")
        
        if len(password)<6:
            messages.error(request, "Password must be at least 6 characters")
            return redirect("signup")

        # continue signup...
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = name
        user.is_active = False
        user.save()
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        #email verification
        current_site = get_current_site(request)
        verify_url = reverse("verify", kwargs={
            "uidb64": uid,
            "token": token
        })
        full_link = f"http://{current_site.domain}{verify_url}"
        
        
        
        subject = "Verify your ViralPrompts account"
        html_message = render_to_string("verify-email.html",{"verify_link": full_link,})
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(subject,plain_message,settings.DEFAULT_FROM_EMAIL,[email],)
        email.attach_alternative(html_message, "text/html")
        email.send()
          






        
        return redirect('check-email')
        
        
        
    
    return render(request, 'signup.html')

def verifyUser(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        
    except (TypeError, ValueError, User.DoesNotExist):
        raise Http404("Invalid verification link")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        raise Http404("Verification link expired")

def checkEmail(request):
    return render(render, 'check-email.html')



#Login User


def loginUser(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier")  # username or email
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=identifier,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    
    return redirect('home')