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
    path('editar_classificacao/<int:campeonato_id>/', views.editar_classificacao, name='editar_classificacao'),
    path('configurar_eliminatorias/<int:campeonato_id>/', views.configurar_eliminatorias, name='configurar_eliminatorias'),
    path('chave_confrontos/<int:campeonato_id>/', views.visualizar_chave_confrontos, name='visualizar_chave_confrontos'),
    path('visualizar_ganhador/<int:campeonato_id>/', views.visualizar_ganhador_unico, name='visualizar_ganhador_unico'),
    path('registrar_resultados_eliminatorias/<int:campeonato_id>/', views.registrar_resultados_eliminatorias, name='registrar_resultados_eliminatorias'),
    path('registrar_penalidades/<int:campeonato_id>/', views.registrar_penalidades, name='registrar_penalidade'),
    path('registrar_penalidades_eliminatorias/<int:campeonato_id>/', views.registrar_penalidades_eliminatorias, name='registrar_penalidades_eliminatorias'),
]
