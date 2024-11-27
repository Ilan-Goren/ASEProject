from django.test import TestCase

from ..solver_functions import piece

class HexPieceTestCase(TestCase):

    def test_visulaise_piece(self):
        for p in piece.pieces.values():
            piece.visualise_piece(p)

    def test_rotate_xy(self):
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        piece.visualise_piece(piece.normalize_transformation(cells))
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            piece.visualise_piece(piece.normalize_transformation(cells))

    def test_reflect(self):
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        piece.visualise_piece(piece.normalize_transformation(cells))
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            reflected_cells = [piece.reflect(c) for c in cells]
            piece.visualise_piece(piece.normalize_transformation(reflected_cells))

    def test_lean(self):
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            leaning_cells = [piece.lean(c) for c in cells]
            piece.visualise_piece(piece.normalize_transformation(leaning_cells))

    def test_transpose_1(self):
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            leaning_cells = [piece.lean(c) for c in cells]
            piece.visualise_piece(piece.normalize_transformation(leaning_cells))
            transposed_leaning_cells = [piece.transpose_lean_1(c) for c in leaning_cells]
            piece.visualise_piece(piece.normalize_transformation(transposed_leaning_cells))

    def test_transpose_2(self):
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        for i in range(5):
            cells = [piece.rotate_xy(c) for c in cells]
            leaning_cells = [piece.lean(c) for c in cells]
            piece.visualise_piece(piece.normalize_transformation(leaning_cells))
            transposed_leaning_cells = [piece.transpose_lean_2(c) for c in leaning_cells]
            piece.visualise_piece(piece.normalize_transformation(transposed_leaning_cells))

    def test_build_transformations(self):
        cells = [(0, 0, 0), (0, 1, 0), (1, 0, 0), (1, 1, 0), (2, 0, 0)]
        transformations = piece.build_transformations(cells)
        for t in transformations:
            print(t)
            piece.visualise_piece(t)

    def test_hex_piece_constructor(self):
        p = piece.Piece(3)
        for t in p.transformations:
            piece.visualise_piece(t)
