from django import forms
from django.shortcuts import render


def home(request):
    if request.method == 'GET':
        return render(request, 'home.html')