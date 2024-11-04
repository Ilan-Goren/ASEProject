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

# Managed list to store solutions.
solutions = manager.list()

# Holds the current process instance, set to None initially.
process = None

selected_boards = []

def home(request):
    """
    Renders the homepage for the Polysphere application.
    
    Args:
        request (HttpRequest): The HTTP request for the home page.
    
    Returns:
        HttpResponse: Renders 'polysphere/home.html' template.
    """
    return render(request, 'polysphere/home.html')

def generator(request):
    """
    Renders the generator page for the Polysphere application.
    
    Args:
        request (HttpRequest): The HTTP request for the generator page.
    
    Returns:
        HttpResponse: Renders 'polysphere/generator.html' with solutions length.
    """
    return render(request, 'polysphere/generator.html', {
        'solutions_len': len(solutions)
    })

def puzzle(request):
    """
    Renders the puzzle page for the Polysphere application.
    
    Args:
        request (HttpRequest): The HTTP request for the puzzle page.
    
    Returns:
        HttpResponse: Renders 'polysphere/puzzle.html' with the following:
        - pieces left in board
        - the board 
        - pieces positions 
        - all solutions 
        - length of all solutions.
    """
    global solutions, selected_boards

    if request.method == 'POST':
        button_pressed = request.POST.get("button") # Get button
        if button_pressed == 'reset_config':
            # if button pressed is 'reset_config' then call function reset board.
            polysphere.reset_board()
            if polysphere.all_solutions_partial_config:
                polysphere.all_solutions_partial_config = []
        return redirect('polysphere_puzzle')
    
    return render(request, 'polysphere/puzzle.html', {
        'pieces': polysphere.pieces_left, 
        'board': polysphere.board,                    
        'positions' : polysphere.piece_positions,       
        'all_solutions_partial_config': polysphere.all_solutions_partial_config,        
        'sol_length': len(polysphere.all_solutions_partial_config) if polysphere.all_solutions_partial_config else 0 
    })


def polysphere_solver(request):
    """
    Handles POST requests for solving partial or complete configurations on the Polysphere puzzle board.

    Args:
        request (HttpRequest): The HTTP request containing the button selection and any configuration data.

    Returns:
        HttpResponseRedirect: Redirects to 'polysphere_puzzle' page with messages for user feedback.
        
    Messages:
        - ERROR: "You have to place at least one piece!" if the board is empty when attempting to find all solutions.
        - ERROR: "Can't find a solution with these pieces :(" if no solution exists for the given configuration.
    """
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
    """
    Handles POST requests to manage solutions and configurations for the Polysphere puzzle and generator, 
    providing options to reset, filter, or display specific solution sets.

    Args:
        request (HttpRequest): The HTTP request containing the selected button action and any filtering parameters.

    Returns:
        HttpResponse: Renders 'polysphere/solutions.html' template with the following context data if filtering or displaying solutions:
            - solutions: Either the filtered solutions or the currently selected solutions.
            - solutions_len: The total number of solutions in 'selected_boards'.
            - start: The start index for filtered display.
            - end: The end index for filtered display, adjusted to be inclusive.

        HttpResponseRedirect: Redirects to the appropriate page if not POST method.

    Button Actions:
        - 'reset': Resets the global solutions list and redirects to the generator page.
        - 'filter_boards': Filters selected boards list based on start and end indices provided by the user.
        - 'partialConfig': Sets 'selected boards' to all solutions from 'polysphere.all_solutions_partial_config'.
        - 'generatorSolutions': Sets 'selected boards' to the global 'solutions' list.
    """
    global solutions        # Get global variable solutions
    global selected_boards  # initialize empty list for filtering
    start = 1               # intialize the start to 1
    filtered_boards = []
    end = 0

    if request.method == 'POST':
        button_pressed = request.POST.get("button") # Get button
        if button_pressed == 'reset':
            # If reset button is pressed empty the solutions list
            solutions = manager.list()
            return redirect('polysphere_generator')

        elif button_pressed == 'filter_boards':
            start = int(request.POST.get('start', '1'))       # Get start number from page.
            end = int(request.POST.get('end')) + 1            # Get end number from page.
            filtered_boards = selected_boards[start:end]      # Store selected boards for display

        elif button_pressed == 'partialConfig':
            selected_boards = polysphere.all_solutions_partial_config

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
    """
    Returns the current count of generated solutions as a JSON response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the key "length" with the count of solutions.
    """
    return JsonResponse({"length": len(solutions)})

# Allows requests without CSRF token.
@csrf_exempt
def start_generator(request):
    """
    Starts the solution generation process if it's not already running.

    Args:
        request (HttpRequest): The HTTP request object.

    Globals:
        process (multiprocessing.Process): The process handling solution generation.
        solutions (list): A list to store generated solutions.

    Returns:
        JsonResponse: 
            - JSON response with {"status": "started"} if the process starts successfully.
            - JSON response with {"status": "already running"} if the process is already running.
            - JSON response with {"error": "Invalid request"} and a 400 status for invalid requests.
    """
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
    """
    Stops the solution generation process if it's currently running.

    Args:
        request (HttpRequest): The HTTP request object, expected to be a POST request.

    Globals:
        process: The process handling solution generation.

    Returns:
        JsonResponse:
            - Redirects to "polysphere_solutions" if the process terminates successfully.
            - JSON response with {"error": "Solver not running"} and a 400 status if the process isn't running.
            - JSON response with {"error": "Invalid request"} and a 400 status for invalid requests.
    """
    global process
    if request.method == 'POST':
        if process and process.is_alive():  
            # Check if Process exists and is running first before terminating
            process.terminate()  # terminate process
            process.join()
            return redirect("polysphere_solutions")
        
        return JsonResponse({"error": "Solver not running"}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

##########################################################################################
#                     PIECES MANIPULATION FUNCTIONS (CALLED FROM JS)                     #
##########################################################################################

# Allows requests without CSRF token.
@csrf_exempt
def place_piece(request):
    """
    Handles POST requests to place a puzzle piece on the board.

    Args:
        request (HttpRequest): The HTTP request containing JSON data with the following keys:
            - "pieceKey": The key for the piece to be placed.
            - "occupiedCells": A list of dictionaries with "row" and "col" indicating cells.

    Returns:
        HttpResponseRedirect: Redirects to 'polysphere_puzzle' with an error message if placing the piece fails.

    Side Effects:
        - Displays an error message to the request if the piece placement is unsuccessful.
    """
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON payload.

        # Extract the piece key and cell positions to place the piece.
        pieceKey = data["pieceKey"]
        posDict = data["occupiedCells"]
        positionPlace = [(cell['row'], cell['col']) for cell in posDict]

        print(f'Key = {pieceKey}')                   # for debugging purposes
        print(f'positionPlace = {positionPlace}')    # for debugging purposes

        # Attempt to place the piece and add an error message if unsuccessful.
        response = polysphere.place_piece(pieceKey, positionPlace)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')

# Allows requests without CSRF token.
@csrf_exempt 
def remove_piece(request):
    """
    Handles POST requests to remove a puzzle piece from the board.

    Args:
        request (HttpRequest): The HTTP request containing JSON data with the following key:
            - "position" (dict): The position of the piece on the board as {"row": int, "col": int}.

    Returns:
        HttpResponseRedirect: Redirects to 'polysphere_puzzle' with an error message if removing the piece fails.

    Side Effects:
        - Displays an error message to the request if the piece removal is unsuccessful.
    """
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
    """
    Handles POST requests to rotate a puzzle piece on the board.

    Args:
        request (HttpRequest): The HTTP request containing JSON data with the following key:
            - "pieceKey": The key of the piece to rotate.

    Returns:
        HttpResponseRedirect: Redirects to 'polysphere_puzzle' with an error message if rotating the piece fails.

    Side Effects:
        - Displays an error message to the request if the piece rotation is unsuccessful.
    """
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
    """
    Handles POST requests to flip a puzzle piece on the board.

    Args:
        request (HttpRequest): The HTTP request containing JSON data with the following key:
            - "pieceKey": The key of the piece to flip.

    Returns:
        HttpResponseRedirect: Redirects to 'polysphere_puzzle' with an error message if flipping the piece fails.

    Side Effects:
        - Displays an error message to the request if the piece flip is unsuccessful.
    """
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON payload.

        # Flip the specified piece and show an error message if unsuccessful.
        pieceKey = data["pieceKey"]
        response = polysphere.flip_piece(pieceKey)
        if not response:
            messages.add_message(request, messages.ERROR, "ERROR", extra_tags='danger')
    return redirect('polysphere_puzzle')