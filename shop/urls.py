from django.urls import path
from . import views
from .api import auth

urlpatterns = [
    path('', views.landing, name='landing'),
    path('product/<slug:slug>/', views.pdp, name='pdp'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('about-us/', views.about_us, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('api/login/', auth.handle_account_authorization, name='api-login'),
    path('api/register/', auth.handle_account_registration, name='api-register'),
]
