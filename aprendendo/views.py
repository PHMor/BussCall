from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

from . import services

import os
from dotenv import load_dotenv

load_dotenv()

@csrf_exempt
def whatsapp_webhook(request):

    if request.method == 'GET':
        verify_token = os.getenv('META_VERIFY_TOKEN')
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        if mode == 'subscribe' and token == verify_token:

            return HttpResponse(challenge)
        
        return HttpResponse("Erro de validação", status=403)

    elif request.method == 'POST':

        data = json.loads(request.body)
        print("tratando mensagem")
        services.tratar_mensagem(data)

        return HttpResponse("EVENT_RECEIVED", status=200)

def home(request):
    HTTP_STRING = render_to_string("home.html")
    return HttpResponse(HTTP_STRING)
