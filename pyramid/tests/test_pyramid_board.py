from django.test import TestCase
from pyramid.solver_functions.pyramid_board import pyramid_board

class PyramidBoardTests(TestCase):

    def setUp(self):
        # Set up a pyramid board with 3 layers before each test
        self.board = pyramid_board(3)

    def test_count_cells(self):
        # Test that the count_cells method returns the correct number of cells
        print(f"Cells: {self.board.cells}")
        self.assertEqual(self.board.count_cells(), 14)  

    def test_convert_to_3D_array(self):
        # Test that the board is correctly converted to a 3D array
        expected_array = [
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[0, 0], [0, 0]],
            [[0]]
        ]  # Updated expected array
        result_array = self.board.convert_to_3D_array()
        print(f"Result Array: {result_array}")
        self.assertEqual(result_array, expected_array)

    def test_convert_from_3D_array(self):
        # Test that a 3D array is correctly converted back to board cells
        new_array = [
            [[6, 7, 8], [9, 10, 11], [12, 13, 14]],
            [[2, 3], [4, 5]],
            [[1]]
        ]  # Updated input array
        self.board.convert_from_3D_array(new_array)
        print(f"Cells after conversion: {self.board.cells}")
        self.assertEqual(self.board.cells[(0, 0, 0)], 6) 
        self.assertEqual(self.board.cells[(2, 2, 2)], 1)

    def test_convert_board_coords_to_array_coords(self):
        # Test that board coordinates are correctly converted to array coordinates
        self.assertEqual(self.board.convert_board_coords_to_array_coords((2, 2, 0)), (1, 1, 0))

    def test_convert_array_coords_to_board_coords(self):
        # Test that array coordinates are correctly converted to board coordinates
        self.assertEqual(self.board.convert_array_coords_to_board_coords((1, 1, 0)), (2, 2, 0))

    def test_is_region_free(self):
        # Test that the is_region_free method correctly identifies free regions
        self.assertTrue(self.board.is_region_free([(0, 0, 0), (2, 0, 0), (0, 2, 0)]))
        self.board.cells[(0, 0, 0)] = 1
        self.assertFalse(self.board.is_region_free([(0, 0, 0), (2, 0, 0), (0, 2, 0)]))

    def test_get_matching_empty_regions(self):
        # Test that the get_matching_empty_regions method correctly identifies matching empty regions
        region = [(0, 0, 0), (2, 0, 0), (0, 2, 0)]
        matching_regions = self.board.get_matching_empty_regions(region)
        print(f"Matching Regions: {matching_regions}")
        self.assertEqual(len(matching_regions), 5)  
        self.board.cells[(0, 0, 0)] = 1
        matching_regions = self.board.get_matching_empty_regions(region)
        print(f"Matching Regions after update: {matching_regions}")
        self.assertEqual(len(matching_regions), 4)  


