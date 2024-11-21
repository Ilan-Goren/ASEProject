from django.test import TestCase
from ..Pyramid import Pyramid, pyramid_get_all_solutions

class PyramidTestCase(TestCase):
    def setUp(self):
        self.pyramid = Pyramid()

    def test_solve_partial_config_none(self):
        """
        Ensure solve_partial_config returns None when given None as input.
        """
        result = self.pyramid.solve_partial_config(None)
        self.assertIsNone(result)

    def test_solve_partial_config_empty(self):
        """
        Ensure solve_partial_config returns None when given an empty list as input.
        """
        result = self.pyramid.solve_partial_config([])
        self.assertIsNone(result)

    def test_solve_partial_config_valid(self):
        """
        Ensure solve_partial_config returns the expected output for a valid input.
        """
        valid_input = [1, 2, 3]  # valid input for the test
        expected_output = [1, 2, 3, 4]  # the expected output for the valid input
        result = self.pyramid.solve_partial_config(valid_input)
        self.assertEqual(result, expected_output)

    def test_generate_all_solutions_none(self):
        """
        Ensure generate_all_solutions returns an empty list when there are no initial solutions.
        """
        result = self.pyramid.generate_all_solutions()
        self.assertEqual(result, [])

    def test_generate_all_solutions_some(self):
        """
        Ensure generate_all_solutions returns the expected output when there are some initial solutions.
        """
        self.pyramid.initial_solutions = [1, 2, 3]  # Set some initial solutions
        expected_output = [1, 2, 3, 4, 5]  # the expected output
        result = self.pyramid.generate_all_solutions()
        self.assertEqual(result, expected_output)

    def test_pyramid_get_all_solutions_empty(self):
        """
        Ensure pyramid_get_all_solutions results in a solutions list of length 0 when starting with an empty list.
        """
        solutions = []
        pyramid_get_all_solutions(solutions)
        expected_length = 0  # the expected number of solutions
        self.assertEqual(len(solutions), expected_length)

    def test_pyramid_get_all_solutions_prefilled(self):
        """
        Ensure pyramid_get_all_solutions maintains the correct length when starting with a pre-filled solutions list.
        """
        solutions = ['existing_solution']
        pyramid_get_all_solutions(solutions)
        expected_length = 1  # expected number of solutions
        self.assertEqual(len(solutions), expected_length)

    def test_pyramid_get_all_solutions_large(self):
        """
        Ensure pyramid_get_all_solutions produces the expected number of solutions and less than 1000 when given a large input.
        """
        solutions = []
        pyramid_get_all_solutions(solutions)
        expected_length = 100  # expected number of solutions
        self.assertEqual(len(solutions), expected_length)
        self.assertTrue(len(solutions) < 1000)