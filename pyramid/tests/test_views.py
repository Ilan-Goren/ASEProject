
from django.test import TestCase, Client
from django.urls import reverse

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/home.html')

    def test_generator_view(self):
        response = self.client.get(reverse('pyramid_generator'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/generator.html')

    def test_puzzle_view(self):
        response = self.client.get(reverse('pyramid_puzzle'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/puzzle.html')

    def test_pyramid_solutions_view_post_generator_solutions(self):
        response = self.client.post(reverse('pyramid_solutions'), {'button': 'generatorSolutions'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pyramid/solutions.html')

    def test_pyramid_solutions_view_post_reset(self):
        response = self.client.post(reverse('pyramid_solutions'), {'button': 'reset'})
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_get_solution_count_view(self):
        response = self.client.post(reverse('get_solution_count'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"length": 0})

    def test_start_generator_view(self):
        response = self.client.post(reverse('start_generator'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "started"})

    def test_stop_generator_view(self):
        response = self.client.post(reverse('stop_generator'))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"error": "Solver not running"})