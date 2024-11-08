from django.urls import path
from polysphere_pyramid import views

urlpatterns = [
    path('', views.home, name='pyramid_home'),
    path('pyramid', views.pyramid, name='pyramid_puzzle'),
    path('solver', views.pyramid_solver, name='pyramid_solver'),
    path('start_generator', views.start_generator, name='pyramid_start_generator'),
    path('stop_generator', views.stop_generator, name='pyramid_stop_generator'),
    path('piece_manipulate', views.piece_manipulate, name='pyramid_piece_manipulate'),
]