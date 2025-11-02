from django.urls import path
from . import views
from .api import auth
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.landing, name='landing'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('product/<slug:slug>/', views.pdp, name='pdp'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('about-us/', views.about_us, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('profile/', views.profile, name='profile'),
    path('profile/address/add/', views.add_address, name='add_address'),
    path('profile/address/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    path('profile/address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete-account/', views.delete_account, name='delete_account'),
    path('api/login/', auth.handle_account_authorization, name='api-login'),
    path('api/register/', auth.handle_account_registration, name='api-register'),
]
