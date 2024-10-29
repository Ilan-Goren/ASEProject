from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import threading
import json
from django.http import JsonResponse
from .Polysphere import Polysphere, get_all_solutions
from .matrix_solver import MatrixSolver

# Initialize the solver
polysphere = Polysphere()
solver = MatrixSolver()
solutions = []
is_running = False

def home(request):
    return render(request, 'polysphere/home.html')

def puzzle(request):
    if request.method == 'POST':
        button_pressed = request.POST.get("button")
        if button_pressed == 'clear_board':
            polysphere.reset_board()
        return redirect('polysphere_puzzle')
    print(polysphere.board)
    return render(request, 'polysphere/puzzle.html', {
        'pieces': polysphere.pieces_left,
        'board': polysphere.board,
        'positions' : polysphere.piece_positions
    })
    

@csrf_exempt 
def place_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        pieceKey = data["pieceKey"]
        posDict = data["occupiedCells"]
        positionPlace = [(dict['row'], dict['col']) for dict in posDict]

        print(f'Key = {pieceKey}')
        print(f'positionPlace = {positionPlace}')

        response = polysphere.place_piece(pieceKey, positionPlace)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')


@csrf_exempt 
def remove_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        position = data["position"]

        position = tuple(position.values())
        for key, pos in polysphere.piece_positions.items():
            for pos_tup in pos:
                if position == pos_tup:
                    pieceKey = key

        response = polysphere.remove_piece(pieceKey)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')

@csrf_exempt 
def rotate_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        pieceKey = data["pieceKey"]
        
        response = polysphere.rotate_piece(pieceKey)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')


@csrf_exempt 
def flip_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        pieceKey = data["pieceKey"]
        
        response = polysphere.flip_piece(pieceKey)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')


def polysphere_solver(request):
    if request.method == 'POST':
        button_pressed = request.POST.get('button')
        if button_pressed == 'solve_board':
            return render(request, 'polysphere/solutions.html', {
            })
        elif button_pressed == 'solve_partial_config':
            response = polysphere.solvePartialConfig()
            if not response:
                messages.add_message(request, messages.ERROR, "Can't find a solution with this these pieces:(", extra_tags='danger')

    return redirect('polysphere_puzzle')


@csrf_exempt
def start_generator(request):
    if request.method == 'POST':
        threading.Thread(target=generate_solutions).start()
        return JsonResponse({"status": "started", "length": len(solutions)})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def get_solution_count(request):
    """Endpoint to get the current length of the solutions list"""
    return JsonResponse({"length": len(solutions)})

def generate_solutions():
    global solutions, is_running
    is_running = True
    get_all_solutions(solutions)

@csrf_exempt
def stop_generator(request):
    if request.method == 'POST':
        global is_running
        is_running = False
        return JsonResponse({"status": "stopped"})