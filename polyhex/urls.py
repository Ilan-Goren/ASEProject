from django.urls import path
from polyhex import views

urlpatterns = [
    path('', views.home, name='polyhex_home'),
    path('puzzle', views.puzzle, name='polyhex_puzzle'),
    path('solutions', views.polyhex_solutions, name='polyhex_solutions'),
    path('generator', views.polyhex_generator, name='polyhex_generator'),
    path('start_generator', views.start_generator, name='polyhex_start_generator'),
    path('stop_generator', views.stop_generator, name='polyhex_stop_generator'),
    path('get-solution-count', views.get_solution_count, name='polyhex_get_solution_count'),
    
]