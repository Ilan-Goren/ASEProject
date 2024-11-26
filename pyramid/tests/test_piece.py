from django.test import TestCase
from pyramid.solver_functions.piece import Piece, build_transformations, rotate_z, rotate_xy, reflect, normalize_transformation, visualise_piece



class TestPieceFunctions(TestCase):
    def setUp(self):
        self.piece = Piece(1)
        self.custom_shape = [(0, 0, 0), (1, 1, 1)]

    def test_build_transformations(self):
        transformations = build_transformations(self.piece.transformations[0])
        self.assertIsNotNone(transformations)
        self.assertTrue(len(transformations) > 0)

    def test_rotate_z(self):
        rotated_shapes = rotate_z(self.custom_shape)
        self.assertIsNotNone(rotated_shapes)
        self.assertEqual(len(rotated_shapes), 4)
        for shape in rotated_shapes:
            self.assertNotEqual(self.custom_shape, shape)

    def test_rotate_xy(self):
        rotated_shape = rotate_xy((1, 2, 3))
        self.assertEqual(rotated_shape, (2, -1, 3))

    def test_reflect(self):
        reflected_shape = reflect((1, 2, 3))
        self.assertEqual(reflected_shape, (-1, 2, 3))

    def test_normalize_transformation(self):
        normalized_shape = normalize_transformation(self.custom_shape)
        self.assertIsNotNone(normalized_shape)
        self.assertEqual(normalized_shape, [(0, 0, 0), (1, 1, 1)])

    def test_visualise_piece(self):
        try:
            visualise_piece(self.custom_shape)
        except Exception as e:
            self.fail(f"visualise_piece raised an exception {e}")

    def test_empty_visualise_piece(self):
        try:
            visualise_piece([])
        except Exception as e:
            self.fail(f"visualise_piece raised an exception {e}")

    def test_invalid_piece_id(self):
        with self.assertRaises(KeyError):
            Piece(99)

    def test_custom_shape_piece(self):
        piece = Piece(99, self.custom_shape)
        self.assertEqual(piece.id, 99)
        self.assertIsNotNone(piece.transformations)
        self.assertIn(self.custom_shape, piece.transformations)

