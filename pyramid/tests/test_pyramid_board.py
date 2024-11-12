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

    def test_count_cells(self):
        board = pyramid_board.pyramid_board(2)
        print(board.count_cells())

    def test_is_region_free(self):
        board = pyramid_board.pyramid_board(2)
        region = [(0, 0, 0), (0, 2, 0), (2, 0, 0), (2, 2, 0), (1, 1, 1)]
        print(board.is_region_free(region))
        region = [(0, 2, 0), (2, 0, 0), (1, 1, 1)]
        print(board.is_region_free(region))
        board.cells[(0, 0, 0)] = 1
        region = [(0, 0, 0), (0, 2, 0), (2, 0, 0), (2, 2, 0), (1, 1, 1)]
        print(board.is_region_free(region))
        region = [(0, 0, 0), (0, 2, 0)]
        print(board.is_region_free(region))
        region = [(0, 2, 0), (2, 0, 0), (2, 2, 0), (1, 1, 1)]
        print(board.is_region_free(region))
        #check region outside possible spaces is false
        region = [(1, 2, 1), (2, 0, 0), (2, 2, 0), (1, 1, 1)]
        print(board.is_region_free(region))

    def test_get_matching_empty_regions(self):
        board = pyramid_board.pyramid_board(2)
        region = [(0, 0, 0), (0, 2, 0), (2, 0, 0)]
        print(board.get_matching_empty_regions(region))
        region = [(0, 2, 0), (1, 1, 1), (2, 0, 0)]
        print(board.get_matching_empty_regions(region))



