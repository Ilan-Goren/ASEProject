from django.test import TestCase

from ..solver_functions import piece

class PieceTestCase(TestCase):
    def test_creating_piece(self):
        piece_one = piece.Piece(11)
        print("transformations:")
        print(piece_one.transformations)

    def test_visulaise_piece(self):
        for p in piece.pieces.values():
            piece.visualise_piece(p)
