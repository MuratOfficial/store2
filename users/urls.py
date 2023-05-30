from django.urls import path
from .views import LoginUserView, UserRegistrationView, UserProfileView, EmailVerificationView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

app_name = 'users'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification')
]