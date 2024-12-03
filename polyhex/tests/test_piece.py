from django.test import TestCase

from ..solver_functions import piece

class PieceTestCase(TestCase):
    """
    Test cases for the Piece class and helper functions functionality.
    """
    def test_visulaise_piece(self):
        """
        Test the visualisation of pieces.

        - Ensures that all pieces can be visualised without errors.

        :raises AssertionError: If any errors occur during visualisation.
        """
        for p in piece.pieces.values():
            piece.visualise_piece(p)
        self.assertTrue(True)

    def test_normalize_transformation(self):
        """
        Test normalization of transformations.

        - Verifies that input transformations are normalized correctly.

        :raises AssertionError: If the output is not as expected.
        """
        self.assertEqual(piece.normalize_transformation([(1, 1, 1)]), [(0, 0, 0)])
        self.assertEqual(piece.normalize_transformation([(-1, -1, -1)]), [(0, 0, 0)])
        self.assertEqual(piece.normalize_transformation([(-1, -1, -1),(3, 3, 3),(5, 4, 2)]), [(0, 0, 0), (4, 4, 4), (6, 5, 3)])

    def test_rotate_xy(self):
        """
        Test rotation of cells in the XY plane.

        - Validates that rotations produce expected results and transformations are accurate.

        :raises AssertionError: If the rotated cells are not as expected.
        """
        cells = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)]
        piece.visualise_piece(piece.normalize_transformation(cells))
        expected_cells = [[(0, 0, 0), (0, 1, 0), (-1, 2, 0), (-1, 3, 0)],
                          [(0, 0, 0), (-1, 1, 0), (-2, 1, 0), (-3, 2, 0)],
                          [(0, 0, 0), (-1, 0, 0), (-1, -1, 0), (-2, -1, 0)],
                          [(0, 0, 0), (0, -1, 0), (1, -2, 0), (1, -3, 0)],
                          [(0, 0, 0), (1, -1, 0), (2, -1, 0), (3, -2, 0)]]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            self.assertTrue(cells in expected_cells)
            piece.visualise_piece(piece.normalize_transformation(cells))

    def test_reflect(self):
        """
        Test reflection of cells.

        - Verifies that reflections are computed accurately and produce expected results.

        :raises AssertionError: If the reflected cells are not as expected.
        """
        cells = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)]
        piece.visualise_piece(piece.normalize_transformation(cells))
        expected_cells = [[(0, 0, 0), (-1, 1, 0), (-1, 2, 0), (-2, 3, 0)],
                            [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0)],
                            [(0, 0, 0), (1, 0, 0), (2, -1, 0), (3, -1, 0)],
                            [(0, 0, 0), (1, -1, 0), (1, -2, 0), (2, -3, 0)],
                            [(0, 0, 0), (0, -1, 0), (-1, -1, 0), (-1, -2, 0)]]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            reflected_cells = [piece.reflect(c) for c in cells]
            self.assertTrue(reflected_cells in expected_cells)
            piece.visualise_piece(piece.normalize_transformation(reflected_cells))

    def test_lean(self):
        """
        Test the `lean` transformation of a piece.

        - Rotates the given cells, applies the lean transformation,
        - Ensures the resulting transformations are among the expected outcomes.
        - Each transformation is also visualized.

        :return: None
        """
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        expected_cells = [[(0, 0, 0), (-1, 0, 1), (0, 0, 1), (-1, 0, 2), (0, 0, 2)],
                            [(0, 0, 0), (-1, 0, 0), (-1, 0, 1), (-2, 0, 1), (-2, 0, 2)],
                            [(0, 0, 0), (0, 0, -1), (-1, 0, 0), (-1, 0, -1), (-2, 0, 0)],
                            [(0, 0, 0), (1, 0, -1), (0, 0, -1), (1, 0, -2), (0, 0, -2)],
                            [(0, 0, 0), (1, 0, 0), (1, 0, -1), (2, 0, -1), (2, 0, -2)]]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            leaning_cells = [piece.lean(c) for c in cells]
            self.assertTrue(leaning_cells in expected_cells)
            piece.visualise_piece(piece.normalize_transformation(leaning_cells))

    def test_transpose_1(self):
        """
        Test the first transposition (for the first additional plane) after leaning.

        - Rotates the given cells, applies the lean transformation,
        - Applies the first type of transposition.
        - Results are validated against a predefined set of transformations and visualized.

        :return: None
        """
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        expected_cells = [[(5, 0, 0), (5, -1, 1), (4, 0, 1), (4, -1, 2), (3, 0, 2)],
                            [(5, 0, 0), (6, -1, 0), (5, -1, 1), (6, -2, 1), (5, -2, 2)],
                            [(5, 0, 0), (6, 0, -1), (6, -1, 0), (7, -1, -1), (7, -2, 0)],
                            [(5, 0, 0), (5, 1, -1), (6, 0, -1), (6, 1, -2), (7, 0, -2)],
                            [(5, 0, 0), (4, 1, 0), (5, 1, -1), (4, 2, -1), (5, 2, -2)]]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            leaning_cells = [piece.lean(c) for c in cells]
            piece.visualise_piece(piece.normalize_transformation(leaning_cells))
            transposed_leaning_cells = [piece.transpose_lean_1(c) for c in leaning_cells]
            self.assertTrue(transposed_leaning_cells in expected_cells)
            piece.visualise_piece(piece.normalize_transformation(transposed_leaning_cells))

    def test_transpose_2(self):
        """
        Test the second transposition (for the second additional plane) after leaning.

        - Rotates the given cells, applies the lean transformation,
        - Applies the second type of transposition.
        - Results are validated against a predefined set of transformations and visualized.

        :return: None
        """
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        expected_cells = [[(0, 5, 0), (0, 5, 1), (0, 4, 1), (0, 4, 2), (0, 3, 2)],
                            [(0, 5, 0), (0, 6, 0), (0, 5, 1), (0, 6, 1), (0, 5, 2)],
                            [(0, 5, 0), (0, 6, -1), (0, 6, 0), (0, 7, -1), (0, 7, 0)],
                            [(0, 5, 0), (0, 5, -1), (0, 6, -1), (0, 6, -2), (0, 7, -2)],
                            [(0, 5, 0), (0, 4, 0), (0, 5, -1), (0, 4, -1), (0, 5, -2)]]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            leaning_cells = [piece.lean(c) for c in cells]
            piece.visualise_piece(piece.normalize_transformation(leaning_cells))
            transposed_leaning_cells = [piece.transpose_lean_2(c) for c in leaning_cells]
            self.assertTrue(transposed_leaning_cells in expected_cells)
            piece.visualise_piece(piece.normalize_transformation(transposed_leaning_cells))

    def test_build_transformations(self):
        """
        Test the generation of all possible transformations of a piece.

        - Validates that the `build_transformations` function generates
          all expected transformations (rotations, reflections, etc.) for a given piece.
        - Each transformation is visualized.

        :return: None
        """
        cells = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)]
        expected_transformations = [[(0, 2, 1), (1, 1, 1), (2, 1, 0), (3, 0, 0)],
                                    [(0, 0, 1), (0, 1, 1), (0, 2, 0), (0, 3, 0)],
                                    [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 2, 0)],
                                    [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 2)],
                                    [(0, 2, 0), (0, 3, 0), (1, 0, 0), (1, 1, 0)],
                                    [(0, 3, 0), (1, 1, 1), (1, 2, 0), (2, 0, 1)],
                                    [(0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 1, 1)],
                                    [(0, 0, 3), (1, 0, 2), (1, 1, 1), (2, 1, 0)],
                                    [(0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0)],
                                    [(0, 0, 2), (1, 0, 1), (2, 0, 1), (3, 0, 0)],
                                    [(0, 0, 1), (1, 0, 1), (2, 0, 0), (3, 0, 0)],
                                    [(0, 1, 2), (1, 1, 1), (2, 0, 1), (3, 0, 0)],
                                    [(0, 0, 2), (0, 1, 1), (0, 2, 1), (0, 3, 0)],
                                    [(0, 2, 0), (1, 1, 0), (2, 1, 0), (3, 0, 0)],
                                    [(0, 0, 2), (0, 0, 3), (1, 0, 0), (1, 0, 1)],
                                    [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2)],
                                    [(0, 0, 3), (1, 0, 1), (1, 0, 2), (2, 0, 0)],
                                    [(0, 0, 3), (0, 1, 1), (0, 1, 2), (0, 2, 0)],
                                    [(0, 1, 0), (1, 1, 0), (2, 0, 0), (3, 0, 0)],
                                    [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 2, 1)],
                                    [(0, 0, 0), (1, 0, 0), (1, 0, 1), (2, 0, 1)],
                                    [(0, 3, 0), (1, 1, 0), (1, 2, 0), (2, 0, 0)],
                                    [(0, 0, 3), (0, 1, 2), (1, 1, 1), (1, 2, 0)],
                                    [(0, 0, 2), (0, 0, 3), (0, 1, 0), (0, 1, 1)]]
        transformations = piece.build_transformations(cells)
        for t in transformations:
            self.assertTrue(t in expected_transformations)
            piece.visualise_piece(t)

    def test_hex_piece_constructor(self):
        """
        Test the constructor for a polyhex piece.

        - Checks that the hex piece constructor creates all expected
          transformations for the piece with ID 4.
        - Each transformation is visualized and compared against the expected results.

        :return: None
        """
        p = piece.Piece(3)
        expected_transformations = [[(0, 0, 2), (0, 0, 3), (0, 0, 4), (0, 1, 1), (0, 2, 0)],
                                    [(0, 0, 4), (1, 0, 3), (2, 0, 0), (2, 0, 1), (2, 0, 2)],
                                    [(0, 0, 2), (0, 1, 2), (0, 2, 2), (0, 3, 1), (0, 4, 0)],
                                    [(0, 0, 2), (1, 0, 2), (2, 0, 2), (3, 0, 1), (4, 0, 0)],
                                    [(0, 0, 4), (0, 1, 3), (0, 2, 0), (0, 2, 1), (0, 2, 2)],
                                    [(0, 2, 0), (1, 1, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)],
                                    [(0, 0, 0), (0, 1, 0), (0, 2, 0), (0, 2, 1), (0, 2, 2)],
                                    [(0, 2, 2), (0, 3, 1), (0, 4, 0), (1, 1, 2), (2, 0, 2)],
                                    [(0, 0, 2), (1, 0, 1), (2, 0, 0), (3, 0, 0), (4, 0, 0)],
                                    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)],
                                    [(0, 0, 0), (0, 0, 1), (0, 0, 2), (1, 0, 2), (2, 0, 2)],
                                    [(0, 4, 0), (1, 3, 0), (2, 0, 2), (2, 1, 1), (2, 2, 0)],
                                    [(0, 0, 2), (0, 0, 3), (0, 0, 4), (1, 0, 1), (2, 0, 0)],
                                    [(0, 2, 0), (0, 3, 0), (0, 4, 0), (1, 1, 0), (2, 0, 0)],
                                    [(0, 2, 2), (1, 1, 2), (2, 0, 2), (3, 0, 1), (4, 0, 0)],
                                    [(0, 4, 0), (1, 3, 0), (2, 0, 0), (2, 1, 0), (2, 2, 0)],
                                    [(0, 2, 0), (1, 2, 0), (2, 2, 0), (3, 1, 0), (4, 0, 0)],
                                    [(0, 2, 2), (1, 2, 1), (2, 2, 0), (3, 1, 0), (4, 0, 0)],
                                    [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 2, 0), (2, 2, 0)],
                                    [(0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 0, 1), (2, 0, 2)],
                                    [(0, 0, 4), (0, 1, 3), (0, 2, 2), (1, 2, 1), (2, 2, 0)],
                                    [(0, 0, 4), (1, 0, 3), (2, 0, 2), (2, 1, 1), (2, 2, 0)],
                                    [(0, 0, 2), (0, 1, 1), (0, 2, 0), (0, 3, 0), (0, 4, 0)],
                                    [(0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 2), (0, 2, 2)]]
        for t in p.transformations:
            self.assertTrue(t in expected_transformations)
            piece.visualise_piece(t)
