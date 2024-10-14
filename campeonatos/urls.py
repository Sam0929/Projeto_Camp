from django.urls import path

from . import views

urlpatterns = [

    path('', views.campeonatos, name='campeonatos'),
]
    