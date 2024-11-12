from django.test import TestCase

from ..solver_functions import piece

class PieceTestCase(TestCase):
    def test_creating_piece(self):
        piece_one = piece.piece(11)

    def test_normalize_transformation(self):
        print(piece.normalize_transformation([(0, 0, 1), (-1, 1, 0), (-1, 1, 2)]))
