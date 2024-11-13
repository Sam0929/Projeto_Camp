from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_campeonatos, name='listar_campeonatos'),
    path('visualizar_desempenho/<int:campeonato_id>/', views.visualizar_desempenho, name='visualizar_desempenho'),
]