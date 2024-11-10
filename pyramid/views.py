from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from multiprocessing import Process, Manager
import json

# Placeholder imports for the 3D solver (to be implemented later)
from .pyramid_solver import PyramidSolver

# Instance of PyramidSolver for managing 3D pyramid configurations.
pyramid_solver = PyramidSolver()

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

def puzzle(request):
    """
    Displays the pyramid puzzle page without referencing undefined attributes.
    """
    return render(request, 'pyramid/puzzle.html')
    
@csrf_exempt
def pyramid_solver(request):
    """
    Handles requests for solving the pyramid configuration.
    """
    if request.method == 'POST':
        button_pressed = request.POST.get('button')
        if button_pressed == 'all_solutions':
            if pyramid_solver.is_board_empty():
                messages.add_message(request, messages.ERROR, "You need to place at least one piece!", extra_tags='danger')
            else:
                response = pyramid_solver.solve_all_partial_config()
                if not response:
                    messages.add_message(request, messages.ERROR, "No solutions found with the current configuration.", extra_tags='danger')
        elif button_pressed == 'complete_board':
            response = pyramid_solver.solve_partial_config()
            if not response:
                messages.add_message(request, messages.ERROR, "No solution found for this configuration.", extra_tags='danger')
    return redirect('pyramid_puzzle')

# @csrf_exempt
# def start_generator(request):
#     """
#     Starts the solution generation process.
#     """
#     global process, solutions
#     if request.method == 'POST':
#         if process:
#             return JsonResponse({"status": "already running"})
        
#         process = Process(target=pyramid_solver.generate_solutions, args=(solutions,))
#         process.start()
#         return JsonResponse({"status": "started"}, status=200)
#     return JsonResponse({"error": "Invalid request"}, status=400)

# @csrf_exempt
# def stop_generator(request):
#     """
#     Stops the solution generation process.
#     """
#     global process
#     if request.method == 'POST':
#         if process and process.is_alive():
#             process.terminate()
#             process.join()
#             return redirect("pyramid_solutions")
#         return JsonResponse({"error": "Solver not running"}, status=400)
#     return JsonResponse({"error": "Invalid request"}, status=400)

# @csrf_exempt
# def piece_manipulate(request):
#     """
#     Handles piece manipulation requests.
#     """
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         action = data.get('action')

#         if action == 'rotate':
#             pieceKey = data["pieceKey"]
#             response = pyramid_solver.rotate_piece(pieceKey)
#             if not response:
#                 messages.add_message(request, messages.ERROR, "Error rotating piece", extra_tags='danger')

#         elif action == 'flip':
#             pieceKey = data["pieceKey"]
#             response = pyramid_solver.flip_piece(pieceKey)
#             if not response:
#                 messages.add_message(request, messages.ERROR, "Error flipping piece", extra_tags='danger')

#         elif action == 'remove':
#             position = tuple(data["position"].values())
#             response = pyramid_solver.remove_piece(position)
#             if not response:
#                 messages.add_message(request, messages.ERROR, "Error removing piece", extra_tags='danger')

#         elif action == 'place':
#             pieceKey = data["pieceKey"]
#             posDict = data["occupiedCells"]
#             positionPlace = [(cell['row'], cell['col']) for cell in posDict]
#             response = pyramid_solver.place_piece(pieceKey, positionPlace)
#             if not response:
#                 messages.add_message(request, messages.ERROR, "Error placing piece", extra_tags='danger')
#         else:
#             messages.add_message(request, messages.ERROR, "Invalid action!", extra_tags='danger')
#         return JsonResponse({'status': 'success'}, status=200)
#     return redirect('pyramid_puzzle')