from django.test import TestCase, Client
from django.urls import reverse
from multiprocessing import Process, Manager
from ..Polysphere import Polysphere
from ..views import polysphere, solutions, process

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

##########################################################################################
#                                  SIMPLE PAGE TESTS                                     #
##########################################################################################

    def test_home_page(self):
        ''' 
        test home page: assert that status code for a get request is 200.
        '''
        response = self.client.get(reverse('polysphere_home'))
        self.assertEqual(response.status_code, 200)

    def test_generator_page(self):
        '''
        test generator page: 
        - assert that status code for a get request is 200.
        - assert that the template used is 'polysphere/generator.html'.
        - assert that the solutions length is 0 when first visited.
        '''
        response = self.client.get(reverse('polysphere_generator'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed('polysphere/generator.html')
        self.assertEqual(response.context['solutions_len'], 0)

    def test_puzzle_page(self):
        '''
        test puzzle page:
        - assert that status code for a get request is 200.
        - assert that the template used is 'polysphere/puzzle.html'.
        - assert all the passed variables are there.
        '''
        response = self.client.get(reverse('polysphere_puzzle'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polysphere/puzzle.html')

        self.assertEqual(response.context['pieces'], polysphere.pieces_left)
        self.assertEqual(response.context['board'], polysphere.board)
        self.assertEqual(response.context['positions'], polysphere.piece_positions)
        self.assertEqual(response.context['all_solutions_partial_config'], polysphere.all_solutions_partial_config)
        self.assertEqual(response.context['sol_length'], len(polysphere.all_solutions_partial_config))

##########################################################################################
#                                  PUZZLE TESTS                                          #
##########################################################################################

    def test_puzzle_reset_button(self):
        '''
        test reset button for puzzle page
        '''
        polysphere.board = ['a', 'b', 'c']
        polysphere.piece_positions = {'A': [(2,3)]}
        polysphere.all_solutions_partial_config = ['board1', 'board2', 'board3']

        response = self.client.post(reverse('polysphere_puzzle'), {
            'button': 'reset_config'
        })
        self.assertEqual(response.status_code, 302)

        self.assertTrue(polysphere.is_board_empty())
        self.assertEqual(polysphere.piece_positions, {})
        self.assertEqual(polysphere.all_solutions_partial_config, [])

    def test_solver_get(self):
        '''
        test solver using get request should be redirected.
        '''
        response = self.client.get(reverse('polysphere_solver'))
        self.assertEqual(response.status_code, 302)

    def test_solver_solving_board(self):
        response = self.client.post(reverse('polysphere_solver'),{
            'button': 'complete_board'
        })
        self.assertTrue(polysphere.is_board_filled)

    def test_solutions_get(self):
        response = self.client.get(reverse('polysphere_solutions'))
        self.assertEqual(response.status_code, 302)

    def test_piece_manipulate(self):
        '''
        test place and remove pieces from puzzle board,
        at first we assert that 'A' is in the pieces not yet placed,
        then mock the post request for placing piece with the essential data,
        then assert again for status code of 200 and that 'A' not longer in pieces left,
        then mock the post request for removing the piece,
        then assert again for status code of 200 and that 'A' is back in pieces left.
        '''
        self.assertIn('A', polysphere.pieces_left)

        response = self.client.post(
            reverse('piece_manipulate'),
            data={
                'action': 'place',
                'pieceKey': 'A',
                'occupiedCells': [{'row': 0, 'col':0}, {'row': 0, 'col': 1}]
            },
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('A', polysphere.pieces_left)

        response = self.client.post(
            reverse('piece_manipulate'),
            data={
                'action': 'remove',
                'position': {'row': 0, 'col':0}
            },
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('A', polysphere.pieces_left)


##########################################################################################
#                                  GENERATOR TESTS                                       #
##########################################################################################
        
    def test_start_generator_get(self):
        '''
        test starting the generator using get should get error and invalid request.
        '''
        response = self.client.get(reverse('start_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request"})

    def test_stop_generator_get(self):
        '''
        test stopping the generator using get should get error and invalid request.
        '''
        response = self.client.get(reverse('stop_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request"})

    def test_start_then_stop_generator(self):
        '''
        test starting the generator using post asserting that we get 'status started' json, 
        then sending post request for stopping generator and asserting a code 302,
        that redirects to another page, in this case 'polysphere_solutions'.
        '''
        response = self.client.post(reverse('start_generator'))
        self.assertEqual(response.json(), {"status": "started"})

        response = self.client.post(reverse('stop_generator'))
        self.assertEqual(response.status_code, 302)

