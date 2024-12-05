from django.test import TestCase
from pyramid.solver_functions.piece import Piece, build_transformations, rotate_z, rotate_xy, reflect, normalize_transformation, visualise_piece

class TestPieceFunctions(TestCase):
    def setUp(self):
        self.piece = Piece(1)
        self.custom_shape = [(0, 0, 0), (1, 1, 1)]

    def test_build_transformations(self):
        # Test that build_transformations returns a non-empty list of transformations for a given piece.
        transformations = build_transformations(self.piece.transformations[0])
        self.assertIsNotNone(transformations)
        self.assertTrue(len(transformations) > 0)

    def test_rotate_z(self):
        # Test that rotate_z returns four different rotations of the custom shape.
        rotated_shapes = rotate_z(self.custom_shape)
        self.assertIsNotNone(rotated_shapes)
        self.assertEqual(len(rotated_shapes), 4)
        for shape in rotated_shapes:
            self.assertNotEqual(self.custom_shape, shape)

    def test_rotate_xy(self):
        # Test that rotate_xy correctly rotates a point around the XY plane.
        rotated_shape = rotate_xy((1, 2, 3))
        self.assertEqual(rotated_shape, (2, -1, 3))

    def test_reflect(self):
        # Test that reflect correctly reflects a point across the YZ plane.
        reflected_shape = reflect((1, 2, 3))
        self.assertEqual(reflected_shape, (-1, 2, 3))

    def test_normalize_transformation(self):
        # Test that normalize_transformation normalizes a shape to start at the origin.
        normalized_shape = normalize_transformation(self.custom_shape)
        self.assertIsNotNone(normalized_shape)
        self.assertEqual(normalized_shape, [(0, 0, 0), (1, 1, 1)])
        
        # Test that a single point is normalized to the origin.
        normalized_single_point = normalize_transformation([(1, 1, 1)])
        self.assertEqual(normalized_single_point, [(0, 0, 0)])

    def test_visualise_piece(self):
        # Test that visualise_piece does not raise an exception for a valid shape.
        try:
            visualise_piece(self.custom_shape)
        except Exception as e:
            self.fail(f"visualise_piece raised an exception {e}")

    def test_empty_visualise_piece(self):
        # Test that visualise_piece does not raise an exception for an empty shape.
        try:
            visualise_piece([])
        except Exception as e:
            self.fail(f"visualise_piece raised an exception {e}")

    def test_invalid_piece_id(self):
        # Test that creating a Piece with an invalid ID raises a KeyError.
        with self.assertRaises(KeyError):
            Piece(99)

    def test_custom_shape_piece(self):
        # Test that a Piece with a custom shape is created correctly.
        piece = Piece(99, self.custom_shape)
        self.assertEqual(piece.id, 99)
        self.assertIsNotNone(piece.transformations)
        self.assertIn(self.custom_shape, piece.transformations)

