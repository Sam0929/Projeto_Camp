from django.urls import path
from . import views

urlpatterns = [
    path('', views.campeonatos, name='campeonatos'),
    path('criar_campeonato/', views.criar_campeonato, name='criar_campeonato'),
    path('editar_campeonato/<int:pk>/', views.editar_campeonato, name='editar_campeonato'),  # Rota para editar campeonato
    path('deletar_campeonato/<int:pk>/', views.deletar_campeonato, name='deletar_campeonato'),  # Rota para deletar campeonato
]
