from django.shortcuts import render

def nqueens(request):
    return render(request, "nqueens/nqueens.html")

def home(request):
    return render(request, "nqueens/home.html")