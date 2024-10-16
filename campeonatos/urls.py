from django.urls import path
from . import views

urlpatterns = [
    path('', views.campeonatos, name='campeonatos'),
    path('criar_campeonato/', views.criar_campeonato, name='criar_campeonato'),
    path('campeonato/<int:pk>/editar/', views.editar_campeonato, name='editar_campeonato'),
    path('participante/<int:pk>/editar/', views.editar_participante, name='editar_participante'),
    path('participante/<int:pk>/excluir/', views.excluir_participante, name='excluir_participante'),
    path('deletar_campeonato/<int:pk>/', views.deletar_campeonato, name='deletar_campeonato'),  # Rota para deletar campeonato
    path('inscricao/<int:pk>/', views.inscrever_participante, name='inscrever_participante'),
    path('campeonato/<int:campeonato_id>/inscrever/', views.inscrever_participante, name='inscrever_participante'),
]
