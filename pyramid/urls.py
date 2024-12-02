from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generator/', views.generator, name='generator'),
    path('puzzle/', views.puzzle, name='puzzle'),
    path('solutions/', views.pyramid_solutions, name='pyramid_solutions'),
    path('get_solution_count/', views.get_solution_count, name='get_solution_count'),
    path('start_generator/', views.start_generator, name='start_generator'),
    path('stop_generator/', views.stop_generator, name='stop_generator'),
]