from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from multiprocessing import Manager, Process
from pyramid.views import process
from unittest.mock import patch, MagicMock

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.manager = Manager()
        self.solutions = self.manager.list()

    def test_home_view(self):
        """
        Test the home view to ensure it returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/home.html')

    def test_generator_view(self):
        """
        Test the generator view to ensure it returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('generator'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/generator.html')
        self.assertIn('solutions_len', response.context)
        self.assertEqual(response.context['solutions_len'], len(self.solutions))

    def test_puzzle_view(self):
        """
        Test the puzzle view to ensure it returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('puzzle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/puzzle.html')

    def test_pyramid_solutions_view_post_generatorSolutions(self):
        """
        Test the pyramid_solutions view with POST request for 'generatorSolutions' button.
        """
        response = self.client.post(reverse('pyramid_solutions'), {'button': 'generatorSolutions'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/solutions.html')
        self.assertIn('solutions', response.context)
        self.assertIn('solutions_len', response.context)
        self.assertEqual(response.context['solutions_len'], len(self.solutions))

    def test_pyramid_solutions_view_post_reset(self):
        """
        Test the pyramid_solutions view with POST request for 'reset' button.
        """
        response = self.client.post(reverse('pyramid_solutions'), {'button': 'reset'})
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('generator')) 

    def test_get_solution_count_view(self):
        """
        Test the get_solution_count view to ensure it returns the correct number of solutions.
        """
        response = self.client.post(reverse('get_solution_count'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"length": len(self.solutions)})

    def test_start_generator_view(self):
        """
        Test the start_generator view to ensure it starts the process correctly.
        """
        response = self.client.post(reverse('start_generator'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"status": "started"})

    @patch('pyramid.views.Process')
    def test_start_generator_view_already_running(self, MockProcess):
        """
        Test the start_generator view to ensure it handles already running process correctly.
        """
        # Simulate process already running
        mock_process = MockProcess.return_value
        mock_process.is_alive.return_value = True

        response = self.client.post(reverse('start_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"status": "already running"})

    @patch('pyramid.views.Process')
    def test_stop_generator_view(self, MockProcess):
        """
        Test the stop_generator view to ensure it stops the process correctly.
        """
        # Simulate process running
        mock_process = MockProcess.return_value
        mock_process.is_alive.return_value = True

        response = self.client.post(reverse('stop_generator'))
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('generator'))  

    @patch('pyramid.views.Process')
    def test_stop_generator_view_not_running(self, MockProcess):
        """
        Test the stop_generator view to ensure it handles the case when no process is running.
        """
        # Simulate process not running
        mock_process = MockProcess.return_value
        mock_process.is_alive.return_value = False

        response = self.client.post(reverse('stop_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"error": "Solver not running"})
