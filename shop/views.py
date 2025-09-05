from django.shortcuts import render

def landing(request):
    return render(request, 'shop/landing.html')
