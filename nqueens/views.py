from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from . import solver
import json

'''
Form to input the value of N for the N-Queens problem.
We use IntegerField to prevent floating-point inputs.
The minimum value is set to 4 and the maximum value is 20, 
which is a reasonable range to avoid performance issues.
'''

class InputNForm(forms.Form):
    n = forms.IntegerField(min_value=4, max_value=20, label='')

# View to handle the home page and render the form
def home(request):
    '''
    Renders the 'home.html' template with an empty form.
    This is the landing page where users input the value of N.
    '''
    if request.method == 'GET':
        return render(request, 'nqueens/home.html', {
            "form": InputNForm()
        })

# View to handle solving the N-Queens problem based on user input
def puzzle(request):
    '''
    Handles the form submission when the user inputs a value for N.
    It checks if the request method is POST and validates the form.
    If the form is valid, it calls the solver to get the N-Queens solution.
    If not, it redirects back to the home page to allow the user to try again.

    Any manipulation of the form data is avoided, as that could lead to
    invalid inputs that might crash the system. 
    '''
    if request.method == 'POST':
        form = InputNForm(request.POST)
        # If the form is valid, proceed to solve the N-Queens problem
        if form.is_valid():
            n = form.cleaned_data["n"] # Get the validated input
            button_pressed = request.POST.get("button")
            if button_pressed == 'go_solution':
                # Call the solver to get the solution for the N-Queens problem
                solution = solver.solve_n_queens(n)
                # Render the 'solution.html' template, passing the solution and N value
                return render(request, 'nqueens/solution.html', {
                    "solution" : solution, "n" : n
                    })
            elif button_pressed == 'go_puzzle':
                    return render(request, 'nqueens/puzzle.html', {
                         "n" : n,
                         "board" : solver.create_empty_board(n),
                         "form": InputNForm()
                    })
        # If the form isn't valid, redirect back to the home page
        else:
            return redirect("nqueens_home")
    # If the request method is GET (e.g., someone manually navigates to /solve), redirect to home
    return redirect("nqueens_home")

def check_solution(request):
    if request.method == 'POST':
        user_board = request.POST.get('user_board')
        board = json.loads(user_board)
        result = solver.check_solution(board)

        if result == True:
            messages.success(request, "Well done! Your solution is correct:)")
        else:
            messages.add_message(request, messages.ERROR, "Your answer is incorrect :(", extra_tags='danger')
    return redirect('nqueens_home')