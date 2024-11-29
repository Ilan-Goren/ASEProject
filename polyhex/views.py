from django.shortcuts import render, redirect
from .solver_functions import board
from .polyhex import solve_partial_config

polyhex_board = board.Board()

def home(request):
    """
    Displays the homepage for the Polysphere Pyramid application.
    """
    return render(request, 'polyhex/home.html')

def puzzle(request):
    """
    Displays the puzzle page for the Polysphere Pyramid application.
    """
    return render(request, 'polyhex/puzzle.html', {
        'board': polyhex_board.board
    })


def polyhex_solutions(request):
    if request.method == "POST":
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

        # solve_partial_config(board, pieces_placed)

        pseudo_board = [\
        [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11], [12, 1, 2, 3], [4, 5, 6], [7, 8], [9]],\
        [[10, 11, 12, 1, 2], [3, 4, 5, 6], [7, 8, 9], [10, 11], [12]],\
        [[1, 2, 3, 4], [5, 6, 7], [8, 9], [10]],\
        [[11, 12, 1], [2, 3], [4]],\
        [[5, 6], [7]],\
        [[8]]\
        ]

        return render(request, 'polyhex/solutions.html', {
            'solutions': [pseudo_board]
        })
    return redirect('polyhex_puzzle')