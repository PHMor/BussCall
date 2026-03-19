"""aprendendo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import home, whatsapp_webhook
from viajens import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', home),
    path('home/', home),
    path('bernardaotarado/', admin.site.urls),
    path('webhook-whatsapp/', whatsapp_webhook, name='whatsapp_webhook'),
    path('clientes', views.clientes_view, name='clientes'),
    path('clientes/criar', views.criar_cliente_view),
    path('clientes/<int:id>/', views.editar_cliente_view),
    path('onibus', views.onibus_view, name='onibus'),
    path('onibus/criar', views.criar_onibus_view),
    path('onibus/<int:id>/', views.editar_onibus_view),
    path('viagem/', views.viagem_view),
    path('validar-viagens/', views.validar_viagem, name='validar_viagens'),
]
