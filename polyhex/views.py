from django.shortcuts import render

def home(request):
    """
    Displays the homepage for the Polysphere Pyramid application.
    """
    return render(request, 'polyhex/home.html')

def puzzle(request):
    """
    Displays the puzzle page for the Polysphere Pyramid application.
    """
    return render(request, 'polyhex/puzzle.html')