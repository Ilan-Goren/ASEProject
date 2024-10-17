from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='nqueens_home'),
    path('solution/', views.solution, name='solution'),
    path('result/', views.check_solution, name='check_solution'),
]