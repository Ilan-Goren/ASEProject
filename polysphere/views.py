from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .Polysphere import Polysphere
from django.http import HttpResponse
from django import forms

# Initialize the solver
polysphere = Polysphere()

class UpdateBoardForm(forms.Form):
    row = forms.IntegerField()
    col = forms.IntegerField()
    piece_key = forms.CharField(max_length=50)

def update_board(request):
    if request.method == 'POST':
        form = UpdateBoardForm(request.POST)
        if form.is_valid():
            row = form.cleaned_data['row']
            col = form.cleaned_data['col']
            piece_key = form.cleaned_data['piece_key']

            success = polysphere.place_piece(piece_key, (row, col))
            if not success:
                return redirect('polysphere_home')
            return redirect('polysphere_home')

    return redirect('polysphere_home')

def home(request):
    return render(request, 'polysphere/home.html')

def puzzle(request):
    if request.method == 'POST':
        button_pressed = request.POST.get("button")
        if button_pressed == 'clear_board':
            polysphere.reset_board()
        elif button_pressed == 'check_solution':
            isIt = polysphere.is_board_filled()
            if isIt:
                messages.success(request, "Board complete!")
                redirect('polysphere_home')
            else:
                messages.add_message(request, messages.ERROR, "Board not complete :(", extra_tags='danger')
        return redirect('polysphere_puzzle')
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
    return render(request, HttpResponse('TO DO'))