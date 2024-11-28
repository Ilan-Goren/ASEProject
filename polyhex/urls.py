from django.urls import path
from polyhex import views

urlpatterns = [
    path('', views.home, name='polyhex_home'),
    path('puzzle', views.puzzle, name='polyhex_puzzle'),
]