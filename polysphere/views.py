from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from multiprocessing import Process, Manager
import json
from django.http import JsonResponse
from .Polysphere import Polysphere, get_all_solutions
from .matrix_solver import MatrixSolver

polysphere = Polysphere()     
solver = MatrixSolver()
manager = Manager()
solutions = manager.list()
# processes = []
process = None

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
        if button_pressed == 'all_solutions':
            return redirect('polysphere_solutions')
        elif button_pressed == 'solve_partial_config':
            response = polysphere.solvePartialConfig()
            if not response:
                messages.add_message(request, messages.ERROR, "Can't find a solution with this these pieces:(", extra_tags='danger')
    return redirect('polysphere_puzzle')

@csrf_exempt
def get_solution_count(request):
    return JsonResponse({"length": len(solutions)})


@csrf_exempt
def start_generator(request):
    global process, solutions
    if request.method == 'POST':
        if process and process.is_alive():
            return JsonResponse({"status": "already running"})

        process = Process(target=get_all_solutions, args=(solutions,))
        process.start()
        return JsonResponse({"status": "started"}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def stop_generator(request):
    global processes
    if request.method == 'POST':
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join()
        processes.clear()
        return JsonResponse({"status": "stopped"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def stop_generator(request):
    global process
    if request.method == 'POST':
        if process and process.is_alive():
            process.terminate()
            process.join()  
            return JsonResponse({"status": "stopped"}, status=200)
        return JsonResponse({"error": "Solver not running"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

def polysphere_solutions(request):
    global solutions
    selected_boards = []
    if request.method == 'POST':
        button_pressed = request.POST.get("button")
        if button_pressed == 'reset':
            solutions = manager.list()

        elif button_pressed == 'show_boards':
            start = int(request.POST.get('start', '1'))
            end = int(request.POST.get('end')) + 1
            
            selected_boards = solutions[start:end]
            return render(request, 'polysphere/solutions.html', {
                'solutions': selected_boards,
                'start': start,
                'end' : end,
                'solutions_len' : len(solutions)
            })
    return render(request, 'polysphere/solutions.html', {
        'solutions': selected_boards if selected_boards else solutions,
        'solutions_len' : len(solutions)
    })