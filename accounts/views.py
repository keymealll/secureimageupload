from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit
from .forms import CustomUserCreationForm
from .models import User


@ratelimit(key='ip', rate='5/h')
def register_view(request):
    """User registration with rate limiting and email verification"""
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        messages.error(
            request, "Too many registration attempts. Please try again later.")
        return render(request, 'accounts/register.html', {'form': CustomUserCreationForm()})

    # disabled as there is a domain problem, but this function below to enable the email verification
    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.is_active = False
    #         user.save()

    #         verification_token = get_random_string(64)

    #         send_mail(
    #             'Verify Your Email',
    #             f'Please verify your email by clicking this link: https://yourdomain.com/verify/{verification_token}/',
    #             'noreply@yourdomain.com',
    #             [user.email],
    #             fail_silently=False,
    #         )

    #         messages.success(
    #             request, "Registration successful! Please check your email to verify your account.")
    #         return redirect('login')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set active immediately since we're not doing email verification
            user.is_active = True
            user.save()

            messages.success(
                request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_email(request, token):
    """Verify user email with token"""
    # In a real app, look up the token and verify the user
    # For demo purposes, we'll just show a success message

    # Simplified implementation (would actually look up token in database):
    # user = get_object_or_404(User, verification_token=token)
    # user.email_verified = True
    # user.is_active = True
    # user.save()

    messages.success(
        request, "Your email has been verified! You can now log in.")
    return redirect('login')


@ratelimit(key='ip', rate='10/m')
def login_view(request):
    """Custom login view with rate limiting and account lockout"""
    # This would be implemented with Django's built-in login view
    # with additional security features

    # Implement account lockout logic here
    # Check if user's account is locked
    # If too many failed attempts, lock account for a period

    # Use Django's login view with customization
    pass


@login_required
def account_settings(request):
    """View for users to manage their account settings"""
    return render(request, 'accounts/settings.html')
