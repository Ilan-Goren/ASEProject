from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from multiprocessing import Process, Manager
import json
from .Pyramid import Pyramid_Solver

# Initialize the Pyramid_Solver instance
pyramid_solver = Pyramid_Solver()

# Manager for multiprocessing to store shared data
manager = Manager()

# Shared list for storing generated solutions
solutions = manager.list()

# Initial process set to None for generator handling
process = None

def home(request):
    """
    Render the homepage for the Polysphere Pyramid application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered homepage template.
    """
    return render(request, 'pyramid/home.html')


def generator(request):
    """
    Render the generator page for the Polysphere Pyramid application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered generator page template with the number of placed pieces
        and solutions.
    """
    return render(request, 'pyramid/generator.html', {
        'pieces_placed_len': len(pyramid_solver.pieces_placed),
        'solutions_len': len(solutions)
    })

def puzzle(request):
    """
    Render the puzzle page for the Polysphere Pyramid application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered puzzle page template.
    """
    return render(request, 'pyramid/puzzle.html')

def pyramid_solutions(request):
    """
    Handle the pyramid solutions page, including displaying solutions, resetting the state,
    and processing partial configuration solutions based on the POST data.

    Args:
        request (HttpRequest): The HTTP request object containing the action to perform.

    Returns:
        HttpResponse: Renders a solutions page, resets the board state, or redirects as needed.
        
    Process:
        - 'generatorSolutions': Displays the list of solutions.
        - 'reset': Clears solutions and resets the board state.
        - 'partialConfigSolutions': Processes partial configuration from the request and updates the board.
    """
    global solutions, process

    if request.method == 'POST':
        button_pressed = request.POST.get('button')
        if button_pressed == 'generatorSolutions':
            return render(request, 'pyramid/solutions.html', {
                'solutions': solutions,
                'solutions_len': len(solutions)
            })
        
        elif button_pressed == 'reset':
            solutions = manager.list()
            pyramid_solver.array_board = []
            pyramid_solver.pieces_placed = []
            process = None
            return redirect('pyramid_generator')
        
        elif button_pressed == 'partialConfigSolutions':
            # solutions = manager.list()
            pyramid_json = request.POST.get('pyramid', 0)
            pieces_placed_json = request.POST.get('piecesPlaced', 0)
            if not pyramid_json or not pieces_placed_json:
                return redirect('pyramid_puzzle')
            
            pyramid = json.loads(pyramid_json)
            pieces_placed = json.loads(pieces_placed_json)
            result = [
                [[int(item) if isinstance(item, str) and item.isdigit() else item for item in sublist] for sublist in group]
                for group in pyramid
            ]

            if not pyramid_json or not pieces_placed_json:
                return redirect('pyramid_home')
            
            pieces_placed = set(int(p) for p in pieces_placed)

            pyramid_solver.array_board = result
            pyramid_solver.pieces_placed = pieces_placed

            # Render the solutions page
            return render(request, 'pyramid/generator.html', {
                'pieces_placed_len': len(pyramid_solver.pieces_placed),
                'solutions_len': len(solutions)
            })
        
    return redirect('pyramid_home')

##########################################################################################
#                           SOLUTIONS GENERATOR FUNCTIONS                                #
##########################################################################################

# Allows requests without CSRF token.
@csrf_exempt
def get_solution_count(request):
    """
    Returns the current count of generated solutions.

    This function checks if the solution generation process is active and, if so, returns the count of generated solutions.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response with the key "length" representing the total count of generated solutions,
                      or a message indicating the generation process is complete if the process is not running.
    """
    global process
    if process and process.is_alive():
        return JsonResponse({"length": len(solutions)})
    else:
        return JsonResponse({"Done": "Generation completed"})


# Allows requests without CSRF token.
@csrf_exempt
def start_generator(request):
    """
    Starts the solution generation process.

    This function checks if the solution generation process is active. If not, it starts a new process to generate solutions.

    Args:
        request (HttpRequest): The HTTP request object.

    Globals:
        process (multiprocessing.Process): The process handling solution generation.
        solutions (list): The list of generated solutions.

    Returns:
        JsonResponse: 
            - A JSON response with {"status": "started"} if the process starts successfully.
            - A JSON response with {"status": "already running"} if a process is already running.
            - A JSON response with {"error": "Invalid request"} for invalid requests.
    """
    global process, solutions # Declare process and solutions as global
    if request.method == 'POST':
        if process: 
            # Check if Process exists and is running first before starting
            return JsonResponse({"status": "already running"}, status=400)

        process = Process(target=pyramid_solver.solve, args=(solutions,))
        process.start()
        return JsonResponse({"status": "started"}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Allows requests without CSRF token.
@csrf_exempt
def stop_generator(request):
    """
    Stops the solution generation process.

    This function terminates the ongoing solution generation process if it is running.

    Args:
        request (HttpRequest): The HTTP request object, expected to be a POST request.

    Globals:
        process (multiprocessing.Process): The process responsible for solution generation.

    Returns:
        JsonResponse:
            - A JSON response with {"Success": "Stopped Successfully"} if the process is stopped successfully.
            - A JSON response with {"error": "Solver not running"} if the process is not running.
            - A JSON response with {"error": "Invalid request"} for invalid requests.
    """
    global process
    if request.method == 'POST':
        if process:  
            # Check if Process exists and is running first before terminating
            process.terminate()  # terminate process
            process.join()
            return JsonResponse({"Success": "Stopped Successfully"}, status=200)
        
        return JsonResponse({"error": "Solver not running"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


