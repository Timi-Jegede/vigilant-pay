from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from .services import LoginService
import secrets
from django.utils import timezone
from datetime import timedelta
from users.models import Profile
from django.http import JsonResponse
# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = LoginService().authenticate_user(request, username, password)

        if user is not None:
            generate_ephemeral_token(request, user)
            profile = Profile.objects.get(user_id=user.id)

            if profile.mfa_enabled:
                return redirect('mfa:verify_mfa')
            else:
                request.session.flush()
                login(request, user)
                
                if user.is_superuser:
                    return redirect('system_admin:admin_index')
                return redirect('users:index')
    else:
        return render(request, 'login/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login/login.html')

def logout_view(request):
    logout(request)

    return redirect('login:login')

def generate_ephemeral_token(request, user):
    user_id = user.id
    ephemeral_token = secrets.token_urlsafe()
    request.session['mfa_token'] = ephemeral_token
    request.session['mfa_user_id'] = user_id
    request.session['mfa_expiry'] = (timezone.now() + timedelta(minutes=5)).isoformat()


