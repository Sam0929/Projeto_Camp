from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # include the campeonatos app urls
    path('home/', include ('pagina_principal.urls')),
    path('campeonatos/', include('campeonatos.urls')),

]
