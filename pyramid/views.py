from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from multiprocessing import Process, Manager
from django.core.serializers import serialize
import json
from .Pyramid import pyramid_get_all_solutions, pyramid_get_partial_config_solutions

# Manager for multiprocessing to store shared data
manager = Manager()
solutions = manager.list()

# Initial process set to None for generator handling
process = None

def home(request):
    """
    Displays the homepage for the Polysphere Pyramid application.
    """
    return render(request, 'pyramid/home.html')

def generator(request):
    """
    Displays the generator page for the Polysphere Pyramid application.
    """
    return render(request, 'pyramid/generator.html', {
        'solutions_len': len(solutions)
    })


def puzzle(request):
    """
    Displays the puzzle page for the Polysphere Pyramid application.
    """
    return render(request, 'pyramid/puzzle.html')

def pyramid_solutions(request):
    """
    Displays the pyramid solutions page.
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
            process = None
            return redirect('pyramid_generator')
        
        elif button_pressed == 'partialConfigSolutions':
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

            results = pyramid_get_partial_config_solutions(result, pieces_placed)
            if not solutions:
                return redirect('pyramid_puzzle')
            solutions = results
            # Render the solutions page
            return render(request, 'pyramid/solutions.html', {
                'solutions': solutions,
                'solutions_len': len(solutions)
            })
        
    return redirect('polysphere_home')

##########################################################################################
#                           SOLUTIONS GENERATOR FUNCTIONS                                #
##########################################################################################

# Allows requests without CSRF token.
@csrf_exempt
def get_solution_count(request):
    """
    Returns the current count of generated solutions.

    This function processes the HTTP request and responds with the number of solutions that have been generated.

    :param request: The HTTP request object.
    :type request: HttpRequest

    :returns: 
        JsonResponse: 
            A JSON response containing the key "length" with the total count of generated solutions.
    """
    return JsonResponse({"length": len(solutions)})

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
        if process: 
            # Check if Process exists and is running first before starting
            return JsonResponse({"status": "already running"}, status=400)

        process = Process(target=pyramid_get_all_solutions, args=(solutions,))
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
        if process and process.is_alive():  
            # Check if Process exists and is running first before terminating
            process.terminate()  # terminate process
            process.join()
            return redirect("pyramid_generator")
        
        return JsonResponse({"error": "Solver not running"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


