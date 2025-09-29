from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('sign-in/', views.sign_in, name='sign-in')
]