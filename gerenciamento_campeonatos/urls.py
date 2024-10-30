from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gerar_tabela/<int:campeonato_id>/', views.gerar_tabela, name='gerar_tabela'),
    path('visualizar_tabela/<int:campeonato_id>/', views.visualizar_tabela, name='visualizar_tabela'),
    path('resultados/<int:campeonato_id>/', views.registrar_resultados, name='registrar_resultados'),
    path('gerar_classificacao/<int:campeonato_id>/', views.gerar_classificacao, name='gerar_classificacao'),
    path('visualizar_classificacao/<int:campeonato_id>/', views.visualizar_classificacao, name='visualizar_classificacao'),
    path('confirmar_classificacao/<int:campeonato_id>/', views.confirmar_classificacao, name='confirmar_classificacao'),
]
