from django.test import TestCase
from .solver import solve_n_queens
from django.test import Client

# List: Some of values for N for the test
N = [4, 5, 6, 7]

class NQueensTestCase(TestCase):
    '''
    test_multiple_queens_horizontal: 
    This test function asserts that for each row there is only one queen.
    If there is more than one the test will fail.
    '''
    def test_multiple_queens_horizontal(self):
        # Loop over list of N to test each one
        for n in N:
            board = solve_n_queens(n) 
            # Assert that the board is not empty
            self.assertNotEqual(board, [])
            for row in range(n):
                self.assertLessEqual(sum(board[row]), 1)
    '''
    test_multiple_queens_vertical: 
    This test function asserts that for each colomn there is only one queen.
    If there is more than one the test will fail.
    '''
    def test_multiple_queens_vertical(self):
        for n in N:
            board = solve_n_queens(n)  
            self.assertNotEqual(board, [])
            for col in range(n):
                self.assertLessEqual(sum([board[row][col] for row in range(n)]), 1)
    '''
    test_multiple_queens_positive_diagonal: 
    This test function asserts that there is only one queen in the center positive diagonal.
    If there is more than one the test will fail.
    '''
    def test_multiple_queens_positive_diagonal(self):
        for n in N:
            board = solve_n_queens(n) 
            self.assertNotEqual(board, [])
            positive_diagonal_count = sum(board[i][i] for i in range(n))
            self.assertLessEqual(positive_diagonal_count, 1)
    '''
    test_multiple_queens_positive_diagonal: 
    This test function asserts that there is only one queen in the center neqative diagonal.
    If there is more than one the test will fail.
    '''
    def test_multiple_queens_negative_diagonal(self):
        for n in N:
            board = solve_n_queens(n)
            self.assertNotEqual(board, [])
            negative_diagonal_count = sum(board[i][n - 1 - i] for i in range(n))
            self.assertLessEqual(negative_diagonal_count, 1)
    '''
    test_home_page: 
    This test function asserts that when the user requests the home page with URL '/',
    It will get a status code of 200, meaning OK
    '''
    def test_home_page(self):
        # Client for test purposes.
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
    '''
    test_solve_output: 
    This test function tests several cases for the solve page.
    Firstly, If the page /solve is requested through 'GET': Assertion for status code 302.
    Secondly, If the page /solve is requested through 'POST': Assertion for status code 200.
    Thirdly, The context of page /solve should which contains.
    '''
    def test_solve_output(self):
        # Client for test purposes.
        c = Client()
        response_get = c.get('/solve/')
        # Check that if request method is get. Assert to being redirected. Code 302.
        self.assertEqual(response_get.status_code, 302)

        valid_data = {'n': 8}
        response_post = c.post('/solve/', valid_data)
        # Check that if request method is post. Assert to OK. Code 200.
        self.assertEqual(response_post.status_code, 200)

        solution = response_post.context["solution"]
        n = response_post.context["n"]

        self.assertNotEqual(solution, [])

        self.assertEqual(sum([sum(solution[i]) for i in range(n)]), n)