from django.test import TestCase
from ..solver_functions.piece import Piece, build_transformations, visualise_piece

class PieceFunctionsTestCase(TestCase):
    def test_piece_initialization(self):
        """
        Test the initialization of a Piece object.
        """
        piece = Piece(1)
        self.assertEqual(piece.id, 1)
        self.assertTrue(piece.transformations)

    def test_build_transformations(self):
        """
        Test the build_transformations function to ensure it generates transformations.
        """
        cells = [(0, 0, 0), (0, 2, 0), (2, 0, 0)]
        transformations = build_transformations(cells)
        self.assertTrue(transformations)

    def test_visualise_piece(self):
        """
        Test the visualise_piece function to ensure it runs without errors.
        """
        cells = [(0, 0, 0), (0, 2, 0), (2, 0, 0)]
        try:
            visualise_piece(cells)
        except Exception as e:
            self.fail(f"visualise_piece raised an exception: {e}")