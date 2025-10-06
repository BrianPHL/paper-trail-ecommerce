from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from ..models import UserProfile

@require_http_methods(["POST"])
def handle_account_authorization(request):
    """Handle login"""
    data = json.loads(request.body)
    email = data.get('email_address')
    password = data.get('password')

    print(User.objects.filter(email=email).exists());
    
    if not User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'err': 'No account found with this email.'}, status=400)
    
    # Check credentials
    user = authenticate(request, username=email, password=password)
    
    if not user:
        return JsonResponse({'success': False, 'err': 'Incorrect password.'}, status=400)
    
    login(request, user)
    return JsonResponse({'success': True, 'redirect': '/'})

