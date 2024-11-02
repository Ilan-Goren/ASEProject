from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from multiprocessing import Process, Manager
import json
from django.http import JsonResponse
from .Polysphere import Polysphere, get_all_solutions
from .solver_functions.matrix_solver import MatrixSolver

# Instance of Polysphere class for managing polysphere configurations.
polysphere = Polysphere()

# Instance of MatrixSolver for solving matrix configurations.
solver = MatrixSolver()

# Manager from multiprocessing for sharing data across processes.
manager = Manager()

# Managed list to store solutions, accessible across processes.
solutions = manager.list()

# Holds the current process instance, set to None initially.
process = None

selected_boards = []

def home(request):
    return render(request, 'polysphere/home.html')

def generator(request):
    return render(request, 'polysphere/generator.html', {
        'solutions_len': len(solutions)
    })

def puzzle(request):
    if request.method == 'POST':
        button_pressed = request.POST.get("button") # Get button
        if button_pressed == 'reset_config':
            # if button pressed is 'reset_config' then call function reset board.
            polysphere.reset_board()
            # Redirect again to the same page.
        return redirect('polysphere_puzzle')
    
    return render(request, 'polysphere/puzzle.html', {
        'pieces': polysphere.pieces_left,               # Pass pieces left to keep track of pieces
        'board': polysphere.board,                      # Pass up to date board
        'positions' : polysphere.piece_positions,       # Pass pieces positions
        'allSolutions': polysphere.allSolutions,        # Pass all board solutions if there is any
        'sol_length': len(polysphere.allSolutions) if polysphere.allSolutions else 0 # pass solutions length
    })


def polysphere_solver(request):
    if request.method == 'POST':
        button_pressed = request.POST.get('button')
        if button_pressed == 'all_solutions':
            if polysphere.is_board_empty():
                 messages.add_message(request, messages.ERROR, "You have to place at least one piece!", extra_tags='danger')
            else:
                response = polysphere.solveAllPartialConfig()
                if not response:
                    messages.add_message(request, messages.ERROR, "Can't find a solution with this these pieces:(", extra_tags='danger')
        elif button_pressed == 'complete_board':
            response = polysphere.solvePartialConfig()
            if not response:
                messages.add_message(request, messages.ERROR, "Can't find a solution with this these pieces:(", extra_tags='danger')
    return redirect('polysphere_puzzle')


def polysphere_solutions(request):
    global solutions     # Get global variable solutions
    global selected_boards # initialize empty list for filtering
    start = 1            # intialize the start to 1
    filtered_boards = []
    end = 0

    if request.method == 'POST':
        button_pressed = request.POST.get("button") # Get button
        if button_pressed == 'reset':
            # Check if boards generated were from partial config or all solutions generator.
            if polysphere.allSolutions:
                # If from partial config reset the list and return to polysphere puzzle.
                polysphere.allSolutions = []
                selected_boards = []
                solutions = manager.list()
                return redirect('polysphere_puzzle')
            else:
                # If from generator reset the list and return to polysphere home.
                solutions = manager.list()
                return redirect('polysphere_generator')

        elif button_pressed == 'filter_boards':
            start = int(request.POST.get('start', '1')) # Get start number from page.
            end = int(request.POST.get('end')) + 1      # Get end number from page.
            filtered_boards = selected_boards[start:end]      # Store selected boards for display

        elif button_pressed == 'partialConfig':
            # solutions = polysphere.allSolutions
            # selected_boards = solutions
            selected_boards = polysphere.allSolutions

        elif button_pressed == 'generatorSolutions':
            selected_boards = solutions

        return render(request, 'polysphere/solutions.html', {
            'solutions': filtered_boards if len(filtered_boards) else selected_boards,
            'solutions_len' : len(selected_boards),
            'start': start,
            'end': end - 1 if end else 0
        })
    return redirect('polysphere_home')

##########################################################################################
#                           SOLUTIONS GENERATOR FUNCTIONS                                #
##########################################################################################

# Allows requests without CSRF token.
@csrf_exempt
def get_solution_count(request):
    return JsonResponse({"length": len(solutions)})

# Allows requests without CSRF token.
@csrf_exempt
def start_generator(request):
    global process, solutions # Declare process and solutions as global
    if request.method == 'POST':
        if process and process.is_alive(): 
            # Check if Process exists and is running first before starting
            return JsonResponse({"status": "already running"})

        process = Process(target=get_all_solutions, args=(solutions,))
        process.start()
        return JsonResponse({"status": "started"}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Allows requests without CSRF token.
@csrf_exempt
def stop_generator(request):
    global process # Declare process as global
    if request.method == 'POST':
        if process and process.is_alive():  
            # Check if Process exists and is running first before terminating
            process.terminate()
            process.join()
            return redirect("polysphere_solutions")
        
        return JsonResponse({"error": "Solver not running"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

##########################################################################################
#                              PIECES MANIPULATION FUNCTIONS                             #
##########################################################################################

# Allows requests without CSRF token.
@csrf_exempt
def place_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON payload.

        # Extract the piece key and cell positions to place the piece.
        pieceKey = data["pieceKey"]
        posDict = data["occupiedCells"]
        positionPlace = [(cell['row'], cell['col']) for cell in posDict]

        print(f'Key = {pieceKey}')
        print(f'positionPlace = {positionPlace}')

        # Attempt to place the piece and add an error message if unsuccessful.
        response = polysphere.place_piece(pieceKey, positionPlace)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')

# Allows requests without CSRF token.
@csrf_exempt 
def remove_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON payload.

        # Identify the piece position to remove.
        position = tuple(data["position"].values())
        for key, pos in polysphere.piece_positions.items():
            if position in pos:
                pieceKey = key

        # Attempt to remove the piece and show an error message if unsuccessful.
        response = polysphere.remove_piece(pieceKey)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')


# Allows requests without CSRF token.
@csrf_exempt 
def rotate_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON payload.

        # Rotate the specified piece and add error message if unsuccessful.
        pieceKey = data["pieceKey"]
        response = polysphere.rotate_piece(pieceKey)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')


# Allows requests without CSRF token.
@csrf_exempt 
def flip_piece(request):
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON payload.

        # Flip the specified piece and show an error message if unsuccessful.
        pieceKey = data["pieceKey"]
        response = polysphere.flip_piece(pieceKey)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')