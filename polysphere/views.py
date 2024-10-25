from django.shortcuts import render
from django.http import request
from django.http import JsonResponse
from .solver import check_solution


def home(request):
    return render(request, 'polysphere/home.html')

def calculate_solution(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        shape = data.get('shape')
        is_solvable = check_solution(shape)
        return JsonResponse({'solvable': is_solvable})
    return JsonResponse({'error': 'Invalid request'}, status=400)