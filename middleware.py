from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Resolve a rota atual para verificar o nome
        current_url_name = resolve(request.path_info).url_name
        
        # Lista de URLs que podem ser acessadas sem login
        public_urls = ['login', 'password_reset', 'password_reset_done','whatsapp_webhook']

        if not request.user.is_authenticated:
            if current_url_name not in public_urls and not request.path.startswith(settings.STATIC_URL):
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)