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

def handle_account_registration(request):
    """Handle user registration"""
    data = json.loads(request.body)
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email_address')
    password = data.get('password')

    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'err': 'An account with this email already exists.'}, status=400)

    # Create new user
    user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
    UserProfile.objects.create(user=user)  # Create associated user profile

    login(request, user)
    return JsonResponse({'success': True, 'redirect': '/'})