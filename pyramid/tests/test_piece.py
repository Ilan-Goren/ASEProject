from django.test import TestCase
from ..solver_functions import piece

class PieceTestCase(TestCase):
    def test_creating_piece(self):
        """
        Test the creation of a Piece object.
        """
        piece_one = piece.Piece(11)
        self.assertTrue(piece_one.transformations)

    def test_visualise_piece(self):
        """
        Test the visualise_piece function to ensure it runs without errors.
        """
        for p in piece.pieces.values():
            try:
                piece.visualise_piece(p)
            except Exception as e:
                self.fail(f"visualise_piece raised an exception: {e}")