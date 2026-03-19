from viajens.models import Cliente
from viajens.models import ViagemCliente
import requests
from django.utils import timezone
import unicodedata
import re

import os
from dotenv import load_dotenv

load_dotenv()

def responder(numero,mensagem):
    url = os.getenv('URL_META_MESSAGES')
    headers = {
        "Authorization": os.getenv('META_TOKEN'),
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response


def normalizar_texto(texto):
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^a-z\s]', '', texto)
    return texto.strip()

def tratar_mensagem(data):
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'statuses' in entry:
            print("Ignorando atualização de status...")
            return "Status ignorado", 200
        from_number = entry['messages'][0]['from']
        from_number = f"{from_number[:4]}9{from_number[4:]}"
        cliente = Cliente.objects.filter(telefone=from_number).first()
        entry_msg = entry['messages'][0]['text']['body'].lower()
        msg_limpa = normalizar_texto(entry_msg)
        
        if cliente:
            # ele eh cliente
            if msg_limpa == "eu vou":
                marcar_viagem(from_number)
            gatilhos = ["nao vou mais", "n vou mais","cancelar"]
            if any(gatilho in msg_limpa for gatilho in gatilhos):
                alterar_viagem(from_number)
        else:
            # ele nao eh cliente
            print("nao eh cliente:")
            mensagem = "VOCE NAO EH CLIENTE"
            responder(from_number,mensagem)
    except KeyError:
        pass
    return

def marcar_viagem(telefone):
    print("Tentando marcar viagem")
    data_hoje = timezone.localtime(timezone.now()).date()
    cliente = Cliente.objects.filter(telefone=telefone).first()
    ja_confirmou = ViagemCliente.objects.filter(cliente_id=cliente.id, data=data_hoje).first()
    if ja_confirmou:
        if ja_confirmou.status == "Cancelada":
            ja_confirmou.status = "Ativo"
            ja_confirmou._change_reason = f"Alterado por whatsapp pelo numero {cliente.telefone}"
            ja_confirmou.save()
            responder(telefone,"Viagem confirmada novamente!")
            return
        print("cliente ja marcou viagem")
        responder(telefone,"Voce ja marcou uma viagem hoje!")
        return
    else:
        nova_viagem = ViagemCliente(data = data_hoje,cliente = cliente, status = "Ativo", onibus = cliente.onibus)
        nova_viagem._change_reason = f"Criado via WhatsApp pelo número {cliente.telefone}"
        nova_viagem.save()
        responder(telefone,"Viagem marcada com sucesso!")
        return

def alterar_viagem(telefone):
    data_hoje = timezone.localtime(timezone.now()).date()
    cliente = Cliente.objects.filter(telefone=telefone).first()
    viagem = ViagemCliente.objects.filter(cliente_id=cliente.id, data=data_hoje).first()
    if viagem and viagem.status == "Ativo":
        print("Cancelado viagem")
        viagem.status = "Cancelada"
        viagem._change_reason = f"Cancelado por whatsapp pelo numero {cliente.telefone}"
        viagem.save()
        responder(telefone,"Viagem cancelada!")
        return
    elif viagem and viagem.status == "Cancelada":
        responder(telefone,"Voce ja cancelou doggg!")
        return
    else:
        responder(telefone,"Voce nem marcou viagem dog ta doidao!")
        return