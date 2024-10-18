from django.shortcuts import render
from django.http import request


def home(request):
    # Pass the range for rows and columns to the template
    return render(request, 'polysphere/home.html', {
        'row_range': range(5),
        'col_range': range(11),
    })