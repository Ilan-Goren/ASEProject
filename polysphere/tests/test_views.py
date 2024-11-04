from django.test import TestCase, Client
from django.urls import reverse
from ..Polysphere import Polysphere

polysphere = Polysphere()

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('polysphere_home'))
        self.assertEqual(response.status_code, 200)

    def test_generator_page(self):
        response = self.client.get(reverse('polysphere_generator'))
        self.assertEqual(response.status_code, 200)

    def test_puzzle_page(self):   
        response = self.client.get(reverse('polysphere_puzzle'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polysphere/puzzle.html')

        self.assertEqual(response.context['pieces'], polysphere.pieces_left)
        self.assertEqual(response.context['board'], polysphere.board)
        self.assertEqual(response.context['positions'], polysphere.piece_positions)
        self.assertEqual(response.context['all_solutions_partial_config'], polysphere.all_solutions_partial_config)
        self.assertEqual(response.context['sol_length'], len(polysphere.all_solutions_partial_config))

    def test_solver_get(self):
        response = self.client.get(reverse('polysphere_solver'))
        self.assertEqual(response.status_code, 302)

    def test_solutions_get(self):
        response = self.client.get(reverse('polysphere_solutions'))
        self.assertEqual(response.status_code, 302)
        
    def test_start_generator_invalid_request(self):
        response = self.client.get(reverse('start_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request"})

    def test_stop_generator_invalid_request(self):
        response = self.client.get(reverse('stop_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request"})

