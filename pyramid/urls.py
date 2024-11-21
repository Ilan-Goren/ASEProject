from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('puzzle', views.puzzle, name='pyramid_puzzle'),
    path('generator', views.generator, name='pyramid_generator'),
    path('solutions', views.pyramid_solutions, name='pyramid_solutions'),
    path('get-solution-count', views.get_solution_count, name='get_solution_count'),
    path('start_generator', views.start_generator, name='start_generator'),
    path('stop_generator', views.stop_generator, name='stop_generator'),
]