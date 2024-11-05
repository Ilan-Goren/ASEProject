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
    Displays the homepage for the Polysphere application.

    :param request: The HTTP request for the homepage.
    :type request: HttpRequest

    :returns: 
        HttpResponse: Renders the 'polysphere/home.html' template.
    """
    return render(request, 'polysphere/home.html')

def generator(request):
    """
    Displays the generator page for the Polysphere application.

    :param request: The HTTP request for the generator page.
    :type request: HttpRequest

    :returns: 
        HttpResponse: Renders 'polysphere/generator.html' with the following context:
            - **solutions length**: The total number of generated solutions.
    """
    return render(request, 'polysphere/generator.html', {
        'solutions_len': len(solutions)
    })

def puzzle(request):
    """
    Displays the puzzle page for the Polysphere application.

    :param request: The HTTP request for the puzzle page.
    :type request: HttpRequest

    :returns: 
        HttpResponse: Renders 'polysphere/puzzle.html' with the following context:
            - **pieces left in board**: Pieces that remain to be placed on the board.
            - **the board**: The current state of the puzzle board.
            - **pieces positions**: The positions of each placed piece.
            - **all solutions**: The complete list of solutions.
            - **length of all solutions**: The total count of possible solutions.
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
    Processes POST requests to solve partial or full configurations on the Polysphere puzzle board.

    This function handles user actions on the puzzle board, such as attempting to solve configurations based on 
    the current piece layout.

    :param request: The HTTP request containing the button selection and any configuration data.
    :type request: HttpRequest

    :returns: 
        HttpResponseRedirect: Redirects the user to the 'polysphere_puzzle' page, providing feedback messages as needed.

    :messages:
        - **ERROR**: "You have to place at least one piece!"  shown if the board is empty when attempting to find solutions.
        - **ERROR**: "Can't find a solution with these pieces :(" shown if no solutions exist for the current configuration.
    """
    if request.method == 'POST':
        button_pressed = request.POST.get('button')
        if button_pressed == 'all_solutions':
            if polysphere.is_board_empty():
                 messages.add_message(request, messages.ERROR, "You have to place at least one piece!", extra_tags='danger')
            else:
                response = polysphere.solve_all_partial_config()
                if not response:
                    messages.add_message(request, messages.ERROR, "Can't find a solution with this these pieces:(", extra_tags='danger')
        elif button_pressed == 'complete_board':
            response = polysphere.solve_partial_config()
            if not response:
                messages.add_message(request, messages.ERROR, "Can't find a solution with this these pieces:(", extra_tags='danger')
    return redirect('polysphere_puzzle')


def polysphere_solutions(request):
    """
    Handles solution management and configuration updates for the Polysphere puzzle.

    This function takes care of different actions you can perform on puzzle solutions, like resetting, filtering, 
    or viewing specific sets of solutions based on user input.

    :param request: The HTTP request that includes the action type and any filtering options.
    :type request: HttpRequest

    :returns: 
        HttpResponse:
            - Renders the 'polysphere/solutions.html' page with relevant data if filtering or displaying solutions:
                - **solutions**: The list of solutions based on current filters or selected options.
                - **solutions_len**: Total number of solutions in 'selected_boards'.
                - **start**: The starting index for displaying filtered solutions.
                - **end**: The ending index for displaying filtered solutions (inclusive).
            - HttpResponseRedirect: Redirects to the home page if the request isn’t a POST.

    Button Actions:
        - **reset**: Clears the global solutions list and takes you back to the generator page.
        - **filter_boards**: Filters the selected boards based on the start and end indices given.
        - **partialConfig**: Loads 'selected_boards' with all solutions from 'polysphere.all_solutions_partial_config'.
        - **generatorSolutions**: Loads 'selected_boards' with the current global list of solutions.
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
            return JsonResponse({"status": "already running"})

        process = Process(target=get_all_solutions, args=(solutions,))
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
            - Redirects to "polysphere_solutions" if the process terminates successfully.
            - Returns a JSON response with a 400 status if the process isn't running.
            - Returns a JSON response with a 400 status for invalid requests.
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
#                     PIECES MANIPULATION FUNCTION (FETCHED FROM JS)                     #
##########################################################################################

@csrf_exempt 
def piece_manipulate(request):
    """
    Process actions to manipulate puzzle pieces based on the user's request.

    This function handles POST requests to modify pieces in the puzzle game. 
    Depending on the action specified in the request body, it can perform one of the following:
    - Rotate a piece
    - Flip a piece
    - Remove a piece
    - Place a piece

    If any action encounters an error, an appropriate error message will be added to the request.

    :param request: The incoming HTTP request containing the action and associated data.
    :type request: HttpRequest

    :returns: 
        HttpResponse: Redirects to the 'polysphere_puzzle' page after processing the request. 
        If the action is not recognized or if a manipulation fails, an error message will be displayed.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')

        # Perform different actions based on the action type
        if action == 'rotate':
            pieceKey = data["pieceKey"]
            # Rotate the specified piece and add error message if unsuccessful.
            response = polysphere.rotate_piece(pieceKey)
            if not response:
                messages.add_message(request, messages.ERROR, "Error Rotating piece", extra_tags='danger')

        elif action == 'flip':
            pieceKey = data["pieceKey"]
            response = polysphere.flip_piece(pieceKey)
            if not response:
                messages.add_message(request, messages.ERROR, "Error Flipping piece", extra_tags='danger')

        elif action == 'remove':
            # Identify the piece position to remove.
            position = tuple(data["position"].values())
            for key, pos in polysphere.piece_positions.items():
                if position in pos:
                    pieceKey = key

            # Attempt to remove the piece and show an error message if unsuccessful.
            response = polysphere.remove_piece(pieceKey)
            if not response:
                messages.add_message(request, messages.ERROR, "Error Removing piece", extra_tags='danger')

        elif action == 'place':
            pieceKey = data["pieceKey"]
            posDict = data["occupiedCells"]
            positionPlace = [(cell['row'], cell['col']) for cell in posDict]

            # Attempt to place the piece and add an error message if unsuccessful.
            response = polysphere.place_piece(pieceKey, positionPlace)
            if not response:
                messages.add_message(request, messages.ERROR, "Error Placing piece", extra_tags='danger')
        else:
            # If non of the known actions
            messages.add_message(request, messages.ERROR, "Incorrect Action!", extra_tags='danger')
        return JsonResponse({'status': 'success'}, status=200)
    return redirect('polysphere_puzzle')