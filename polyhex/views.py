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
    """
    return render(request, 'polyhex/home.html')

def puzzle(request):
    global solutions
    """
    Displays the puzzle page for the Polysphere Pyramid application.
    """
    return render(request, 'polyhex/puzzle.html', {
        'board': polyhex_board.board,
        'solutions_len': len(solutions),
    })

def polyhex_generator(request):
    global solutions
    """
    Displays the puzzle page for the Polysphere Pyramid application.
    """
    return render(request, 'polyhex/generator.html', {
        'solutions_len': len(solutions),
        'pieces_placed_len': len(polyhex_solver.pieces_placed)
    })


def polyhex_solutions(request):
    global solutions

    if request.method == "POST":
        button_pressed = request.POST.get('button')
        if button_pressed == 'go_solutions':
            if solutions and not process.is_alive():
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
    global process, solutions
    """
    Returns the current count of generated solutions.

    This function processes the HTTP request and responds with the number of solutions that have been generated.

    :param request: The HTTP request object.
    :type request: HttpRequest

    :returns: 
        JsonResponse: 
            A JSON response containing the key "length" with the total count of generated solutions.
    """

    if process and process.is_alive():
        print('YAAAY')
        return JsonResponse({"length": len(solutions)})
    else:
        return JsonResponse({"Done": "Generation completed"})


# Allows requests without CSRF token.
@csrf_exempt
def start_generator(request):
    """
    Handles the HTTP request to initiate the solution generation process.

    This function checks if the solution generation process is active and, if not, starts a new process. 
    It manages incoming requests and ensures only one process is active at a time.

    :param request: The HTTP request object.
    :type request: HttpRequest

    :global process: The multiprocessing.Process instance that handles solution generation.
    :global solutions: A list for storing generated solutions.

    :returns: 
        JsonResponse:
            - A JSON response with {"status": "started"} and a 200 status code if the process starts successfully.
            - A JSON response with {"status": "already running"} if the process is already active.
            - A JSON response with {"error": "Invalid request"} and a 400 status code for invalid requests.
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

    This function handles a POST request to terminate the ongoing solution generation process. 
    It checks the state of the process and responds accordingly.

    :param request: The HTTP request object, expected to be a POST request.
    :type request: HttpRequest

    :globals: 
        process: The process responsible for handling solution generation.

    :returns: 
        JsonResponse:
            - Redirects to "pyramid_solutions" if the process terminates successfully.
            - Returns a JSON response with a 400 status if the process isn't running.
            - Returns a JSON response with a 400 status for invalid requests.
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