from django.test import TestCase
from ..solver_functions.piece import Piece, build_transformations, visualise_piece

class PieceFunctionsTestCase(TestCase):
    def test_piece_initialization(self):
        """
        Verify that a Piece object is initialized correctly with the given ID and transformations.
        """
        piece = Piece(1)
        self.assertEqual(piece.id, 1)
        self.assertIsNotNone(piece.transformations)

    def test_build_transformations(self):
        """
        Ensure that the build_transformations function generates the correct transformations for given cells.
        """
        cells = [(0, 0, 0), (0, 2, 0), (2, 0, 0)]
        expected_transformations = [
            [(0, 0, 0), (0, 2, 0), (2, 0, 0)],
            [(0, 0, 0), (0, -2, 0), (-2, 0, 0)],
            # Add more transformations as needed
        ]
        transformations = build_transformations(cells)
        self.assertEqual(transformations, expected_transformations)

    def test_visualise_piece(self):
        """
        Check that the visualise_piece function runs without errors for given cells.
        """
        cells = [(0, 0, 0), (0, 2, 0), (2, 0, 0)]
        try:
            visualise_piece(cells)
        except Exception as e:
            self.fail(f"visualise_piece raised an exception: {e}")