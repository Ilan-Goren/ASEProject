from django.urls import path
from polysphere import views


urlpatterns = [
    path('', views.home, name='polysphere_home'),
    path('puzzle', views.puzzle, name='polysphere_puzzle'),
    path('solver', views.polysphere_solver, name='polysphere_solver'),
    path('get-solution-count', views.get_solution_count, name='get_solution_count'),
    path('start_generator', views.start_generator, name='start_generator'),
    path('stop_generator', views.stop_generator, name='stop_generator'),
    path('solutions', views.polysphere_solutions, name='polysphere_solutions'),
    path('generator', views.generator, name='polysphere_generator'),
    path('piece_manipulate', views.piece_manipulate, name='piece_manipulate')
]