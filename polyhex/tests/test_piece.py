from django.test import TestCase

from ..solver_functions import piece

class PieceTestCase(TestCase):

    def test_visulaise_piece(self):
        for p in piece.pieces.values():
            piece.visualise_piece(p)
        self.assertTrue(True)

    def test_normalize_transformation(self):
        self.assertEqual(piece.normalize_transformation([(1, 1, 1)]), [(0, 0, 0)])
        self.assertEqual(piece.normalize_transformation([(-1, -1, -1)]), [(0, 0, 0)])
        self.assertEqual(piece.normalize_transformation([(-1, -1, -1),(3, 3, 3),(5, 4, 2)]), [(0, 0, 0), (4, 4, 4), (6, 5, 3)])

    def test_rotate_xy(self):
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
