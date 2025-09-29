from django.shortcuts import render

def landing(request):
    return render(request, 'shop/landing.html')

def sign_in(request):
    return render(request, 'shop/sign-in.html')
