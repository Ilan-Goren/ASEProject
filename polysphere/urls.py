from django.urls import path
from django import views


urlPatterns = [
    path('', views.home, name='home')
]