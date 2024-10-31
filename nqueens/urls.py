from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='nqueens_home'),
    path('/puzzle', views.puzzle, name='puzzle'),
    path('/result', views.check_solution, name='check_solution'),
]