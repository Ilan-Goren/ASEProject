from django.urls import path
from polysphere import views


urlpatterns = [
    path('', views.home, name='polysphere_home'),
    path('/puzzle', views.puzzle, name='polysphere_puzzle'),
    path('/place_piece', views.place_piece, name='place_piece'),
    path('/remove_piece', views.remove_piece, name='remove_piece'),
    path('/rotate_piece', views.rotate_piece, name='rotate_piece'),
    path('/flip_piece', views.flip_piece, name='flip_piece'),
    path('/solver', views.polysphere_solver, name='polysphere_solver'),

    
]