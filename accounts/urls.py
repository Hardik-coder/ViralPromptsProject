from django.urls import path
from accounts import views

urlpatterns = [
    path('signup/', views.signupUser, name='signup'),
    path('login/', views.loginUser, name='login'),
    path('verify/<uidb64>/<token>', views.verifyUser, name="verify"),
    path('check-email/', views.checkEmail, name='check-email')
    

]