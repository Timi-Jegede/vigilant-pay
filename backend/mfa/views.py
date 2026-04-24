from django.shortcuts import render, redirect
from .services import MFAService
from .models import BackupCode
from users.models import Profile
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password, make_password
import base64
import secrets
from django.contrib.auth.models import User
from users.models import Profile
from cryptography.fernet import Fernet
import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.conf import settings
from django.urls import reverse

# Create your views here.
def verify_mfa(request):
    error_message = None
    service = MFAService()
    template = service.get_template()

    if request.method == 'POST':
        mfa_session_time = datetime.fromisoformat(request.session['mfa_expiry'])

        if (timezone.now() < mfa_session_time) and (request.session['mfa_token']):
            otp_code = request.POST.get('otp-code')
            token = otp_code
            user_id = request.session['mfa_user_id']
            user = User.objects.get(id=user_id)
            success, message = MFAService.verify_token(user, token)

            if success:
                request.session.flush()
                login(request, user)
                return redirect('system_admin:admin_index') if request.user.is_superuser else 'users:index'
        
            else:
                error_message = message

    return render(request, template, {'error': error_message})

def setup_backup_codes(request):
    user_backup_codes = MFAService.generate_backup_codes()

    request.user.backup_code.all().delete()
    for user_backup_code in user_backup_codes:
       BackupCode.objects.create(
            user=request.user,
            hashed_codes=make_password(user_backup_code),
            is_used=False
        )
    
    return render(request, 'authentication/show-backup-codes.html', {'user_backup_codes': user_backup_codes})

def incomplete_mfa_setup(request):
    profile = request.user.profile
    otp_secret = profile.otp_secret
    mfa_enabled = profile.mfa_enabled

    if otp_secret and mfa_enabled == False:
        return JsonResponse({'incomplete_mfa_setup': 'Setup Not Complete'})

def complete_mfa_setup(request): 
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            token = data.get('verificationCode')

            verify_token, message = MFAService.verify_token(request.user, token)

            if verify_token:
                profile = request.user.profile
                profile.mfa_enabled = True
                profile.mfa_configured = True
                profile.save()

                url = reverse('system_admin:admin_security')
                return JsonResponse({'settings': url})
            else:
                return JsonResponse({'message': message})
    except KeyError as e:
        return HttpResponseBadRequest(f'Missing field required: {str(e)}')

def setup_uri(request):
    profile = request.user.profile

    if profile.otp_secret:
        secret_key = profile.secret_key()
        qrcode_image = MFAService.qrcode_image_generator(request.user.email, secret_key)

        return render(request, 'authentication/mfa-setup.html', {'qrcode_image': qrcode_image})
    else:
        fernet_key = settings.FERNET_KEY
        fernet_encryption = Fernet(fernet_key)

        secret_key = MFAService.generate_secret_key()

        encrypted_secret_key = fernet_encryption.encrypt(secret_key.encode())
        decoded_secret_key = encrypted_secret_key.decode()
        profile.otp_secret = decoded_secret_key
        profile.save()

        qrcode_image = MFAService.qrcode_image_generator(request.user.email, secret_key)
        
        return render(request, 'authentication/mfa-setup.html', {'qrcode_image': qrcode_image})

def setup_mfa(request):
    if request.method == 'POST':
        password = request.POST.get('user-password')

        if check_password(password, request.user.password):
            return setup_backup_codes(request)
        else:
            return render(request, 'authentication/check-password.html', {'error_message':'Password incorrect! Try again.'})

    return render(request, 'authentication/check-password.html')

def manage_mfa(request):
    return render(request, 'authentication/mfa-information.html')

def set_mfa_status(request):
    raw_status = request.POST.get('mfa_status')
    mfa_status = raw_status.lower() in ['true', 'on', 1]

    profile = request.user.profile
    profile.mfa_enabled = mfa_status
    profile.save()
    mfa_enabled = profile.mfa_enabled

    return JsonResponse({'mfa_status': mfa_enabled})

def get_mfa_configured_status(request):
    profile = request.user.profile
    mfa_configured_status = profile.mfa_configured

    return JsonResponse({'mfa_configured_status': mfa_configured_status})