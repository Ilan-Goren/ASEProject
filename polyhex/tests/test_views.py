from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from unittest.mock import patch, Mock

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

##########################################################################################
#                                  SIMPLE PAGE TESTS                                     #
##########################################################################################

    def test_home_view(self):
        """
        Test the home view to ensure it returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('polyhex_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polyhex/home.html')

    @patch('polyhex.views.solutions')
    def test_generator_view(self, MockSolutions):
        """
        Test the generator view to ensure it returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('polyhex_generator'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polyhex/generator.html')
        self.assertIn('solutions_len', response.context)
        self.assertEqual(response.context['solutions_len'], len(MockSolutions.return_value))

    def test_puzzle_view(self):
        """
        Test the puzzle view to ensure it returns a 200 status code and uses the correct template.
        """
        response = self.client.get(reverse('polyhex_puzzle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polyhex/puzzle.html')

##########################################################################################
#                               VIEWS SOLUTIONS TESTS                                    #
##########################################################################################
 
    @patch('polyhex.views.solutions')
    def test_polyhex_solutions_view_post_generatorSolutions(self, MockSolutions):
        """
        Test the polyhex_solutions view with POST request for 'generatorSolutions' button.
        """
        solutions = MockSolutions.return_value

        response = self.client.post(reverse('polyhex_solutions'), {'button': 'go_solutions'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polyhex/solutions.html')
        self.assertIn('solutions', response.context)
        self.assertIn('solutions_len', response.context)
        self.assertEqual(response.context['solutions_len'], len(solutions))


    def test_polyhex_solutions_view_post_reset(self):
        """
        Test the polyhex_solutions view with POST request for 'reset' button.
        """
        response = self.client.post(reverse('polyhex_solutions'), {'button': 'reset'})
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse('polyhex_generator'))

    @patch('polyhex.views.process')
    @patch('polyhex.views.solutions')
    def test_get_solution_count_view(self, MockProcess, MockSolutions):
        """
        Test the get_solution_count view to ensure it returns the correct number of solutions.
        """

        process = MockProcess.return_value
        process.is_alive.return_value = True

        response = self.client.get(reverse('polyhex_get_solution_count'))
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"length": len(MockSolutions.return_value)})

    @patch('polyhex.views.process', None)
    def test_get_solution_count_not_running_view(self):
        """
        Test the get_solution_count view to ensure it returns the correct number of solutions.
        """

        response = self.client.get(reverse('polyhex_get_solution_count'))
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"Done": "Generation completed"})


##########################################################################################
#                               VIEWS GENERATOR TESTS                                    #
##########################################################################################

    @patch('polyhex.views.process', None)
    def test_start_generator_view(self):
        """
        Test the start_generator view to ensure it starts the process correctly.
        """
        response = self.client.post(reverse('polyhex_start_generator'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"status": "started"})
        
        # Stopping
        response = self.client.post(reverse('polyhex_stop_generator'))
        self.assertEqual(response.status_code, 200)

    @patch('polyhex.views.process')
    def test_start_generator_view_already_running(self, MockProcess):
        """
        Test the start_generator view to ensure it handles already running process correctly.
        """
        mock_process = MockProcess.return_value
        mock_process.is_alive.return_value = True

        response = self.client.post(reverse('polyhex_start_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.json(), {"status": "already running"})

    @patch('polyhex.views.process')
    def test_stop_generator_view(self, MockProcess):
        """
        Test the stop_generator view to ensure it stops the process correctly.
        """
        mock_process = MockProcess.return_value
        mock_process.is_alive.return_value = True

        response = self.client.post(reverse('polyhex_stop_generator'))
        self.assertEqual(response.status_code, 200)

    @patch('polyhex.views.process', None)
    def test_stop_generator_view_not_running(self):
        """
        Test the stop_generator view to ensure it handles the case when no process is running.
        """