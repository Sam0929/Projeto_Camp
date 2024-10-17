from django.urls import path
from . import views

urlpatterns = [
    path('', views.gerenciamento_campeonato, name='gerenciamento_campeonato'),
]
