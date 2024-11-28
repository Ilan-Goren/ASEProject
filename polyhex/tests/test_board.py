from django.test import TestCase

from ..solver_functions import board

class BoardTestCase(TestCase):
    def test_board(self):
        b = board.Board()
        print(b.board)
        print(b.count_cells())

    def test_is_region_free(self):
        b = board.Board()
        print(b.is_region_free([(0,0,0),(1,0,0),(0,0,5)]))

    def test_get_matching_empty_regions(self):
        b = board.Board()
        print(b.get_matching_empty_regions([(0,0,0),(1,0,0)]))