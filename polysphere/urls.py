from django.urls import path
from polysphere import views


urlpatterns = [
    path('', views.home, name='polysphere_home')
]