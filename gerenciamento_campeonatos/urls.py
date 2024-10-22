from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Página principal do gerenciamento
    path('gerar_tabela/<int:campeonato_id>/', views.gerar_tabela, name='gerar_tabela'),
    path('visualizar_tabela/<int:campeonato_id>/', views.visualizar_tabela, name='visualizar_tabela'),
    path('resultados/<int:campeonato_id>/', views.registrar_resultados, name='registrar_resultados'),
    path('gerar_tabela/<int:campeonato_id>/', views.gerar_tabela, name='gerar_tabela'),
]
