from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifique se o usuário não está autenticado e se a URL pertence a um app específico
        if not request.user.is_authenticated and self.is_protected_app(request):
            return redirect(reverse('login'))  # Redireciona para a página de login

        response = self.get_response(request)
        return response

    def is_protected_app(self, request):
        # Define os apps para os quais a autenticação é obrigatória
        protected_apps = ['gerenciamento_campeonatos', 'desempenho', 'campeonatos']  # Substitua pelos seus apps

        # Verifica se o caminho da URL inclui o nome do app
        for app in protected_apps:
            if request.path.startswith(f'/{app}/'):
                return True

        return False
    
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_superuser):
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
