from django.shortcuts import render, redirect
from .solver_functions import board
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .polyhex import Polyhex_Solver
from multiprocessing import Process, Manager

polyhex_board = board.Board()

polyhex_solver = Polyhex_Solver()

manager = Manager()
solutions = manager.list()

# Initial process set to None for generator handling
process = None

def home(request):
    """
    Displays the homepage for the Polysphere Pyramid application.

    This view renders the homepage, where users can start interacting with the Polyhex puzzle.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered homepage template.
    """
    return render(request, 'polyhex/home.html')

def puzzle(request):
    """
    Displays the puzzle page for the Polysphere Pyramid application.

    This view renders the puzzle page where users can interact with the current puzzle, 
    viewing the current board state and the number of solutions generated.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered puzzle page template.
    """
    global solutions
    return render(request, 'polyhex/puzzle.html', {
        'board': polyhex_board.board,
        'solutions_len': len(solutions),
    })

def polyhex_generator(request):
    """
    Displays the generator page for the Polysphere Pyramid application.

    This view renders the generator page where users can generate solutions for the Polyhex puzzle. 
    It also provides the current number of solutions and the number of pieces placed.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered generator page template.
    """
    global solutions

    return render(request, 'polyhex/generator.html', {
        'solutions_len': len(solutions),
        'pieces_placed_len': len(polyhex_solver.pieces_placed)
    })


def polyhex_solutions(request):
    """
    Handles the solution generation and reset actions for the Polyhex puzzle.

    This view processes POST requests for generating solutions, resetting the puzzle state, and saving a new puzzle configuration.
    Depending on the button pressed, it either renders the solutions page, resets the puzzle, or saves the new puzzle state.

    Args:
        request (HttpRequest): The HTTP request object containing form data.

    Returns:
        HttpResponseRedirect: A redirect response to another view, either the solutions page or the puzzle generator.
    """
    global solutions

    if request.method == "POST":
        button_pressed = request.POST.get('button')
        if button_pressed == 'go_solutions':
            if solutions:
                return render(request, 'polyhex/solutions.html', {
                    'solutions': solutions,
                    'solutions_len': len(solutions)
                })
        elif button_pressed == 'reset':
            solutions = manager.list()
            polyhex_solver.board = None
            polyhex_solver.pieces_placed = []
            return redirect('polyhex_generator')

        elif button_pressed == 'save_puzzle':
            board = []
            pieces_placed = set()

            for layer_num in range(6):
                layer = []
                for row_num in range(6 - layer_num):
                    row = []
                    for col_num in range(6 - layer_num - row_num):
                        input_name = f'cell-{layer_num}-{row_num}-{col_num}'
                        value = request.POST.get(input_name, '')
                        row.append(int(value) if value.isdigit() else 0)
                        if value.isdigit():
                            value = int(value)
                            pieces_placed.add(value)
                    layer.append(row)
                board.append(layer)
            print(board)
            print(pieces_placed)

            polyhex_solver.board = board
            polyhex_solver.pieces_placed = pieces_placed
            solutions = manager.list()
            return redirect('polyhex_generator')

    return redirect('polyhex_puzzle')


##########################################################################################
#                           SOLUTIONS GENERATOR FUNCTIONS                                #
##########################################################################################

# Allows requests without CSRF token.
@csrf_exempt
def get_solution_count(request):
    """
    Returns the current count of generated solutions.

    This view returns the current number of generated solutions, checking if the solution generation process is still active. 
    If the process is complete, a message indicating that the generation is finished is returned.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing:
            - {"length": <count>} if the process is active.
            - {"Done": "Generation completed"} if the process is not running.
    """
    global process, solutions

    if process and process.is_alive():
        print('YAAAY')
        return JsonResponse({"length": len(solutions)})
    else:
        return JsonResponse({"Done": "Generation completed"})


# Allows requests without CSRF token.
@csrf_exempt
def start_generator(request):
    """
    Starts the solution generation process.

    This view initiates the solution generation process by starting a new process, if one is not already running. 
    It ensures that only one process can be active at a time.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response indicating the status of the process:
            - {"status": "started"} if the process starts successfully.
            - {"status": "already running"} if the process is already active.
            - {"error": "Invalid request"} for invalid requests.
    """
    global process, solutions # Declare process and solutions as global
    if request.method == 'POST':
        if process and process.is_alive(): 
            # Check if Process exists and is running first before starting
            return JsonResponse({"status": "already running"}, status=400)

        process = Process(target=polyhex_solver.solve, args=(solutions,))
        process.start()
        return JsonResponse({"status": "started"}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

# Allows requests without CSRF token.
@csrf_exempt
def stop_generator(request):
    """
    Stops the solution generation process if it is currently running.

    This view terminates the ongoing solution generation process upon a POST request and ensures the process is stopped properly.

    Args:
        request (HttpRequest): The HTTP request object, expected to be a POST request.

    Returns:
        JsonResponse: A JSON response indicating the result of the stop action:
            - {"Success": "Stopped Successfully"} if the process is terminated successfully.
            - {"error": "Solver not running"} if no process is active.
            - {"error": "Invalid request"} for invalid requests.
    """
    global process
    if request.method == 'POST':
        if process and process.is_alive():
            # Check if Process exists and is running first before terminating
            process.terminate()  # terminate process
            process.join()
            return JsonResponse({"Success": "Stopped Successfully"}, status=200)
        
        return JsonResponse({"error": "Solver not running"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)