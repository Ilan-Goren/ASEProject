from django.test import TestCase

from ..solver_functions import pyramid_board

class PyramidBoardTestCase(TestCase):
    def test_creating_board(self):
        board = pyramid_board.pyramid_board(5)

        #arrayBoard = board.convert_to_3D_array()

        #print(arrayBoard)

        array_board = [
         [[1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0]],
         [[0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],
         [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
         [[0, 0],
         [0, 0]],
         [[0]]
        ]

        board.convert_from_3D_array(array_board)
        arr = board.convert_to_3D_array()
        #print(arr)

