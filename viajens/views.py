from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Onibus, ViagemCliente, Viagem
from django.db.models import Count, F
from django.utils import timezone
from . import forms
from datetime import time
from datetime import date

# Create your views here.
def criar_cliente_view(request):
    form = forms.ClienteForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('clientes')
    return render(request, 'viajens/criar_clientes.html', {'form': form})

def clientes_view(request):
    try:
        clientes = Cliente.objects.all()
    except:
        clientes = None
    context = {'clientes': clientes}
    HTTP_STRING = render(request, 'viajens/clientes.html',context=context)
    return HttpResponse(HTTP_STRING)

def editar_cliente_view(request,id = None):
    if id is not None:
        cliente = get_object_or_404(Cliente, id=id)
        form = forms.ClienteForm(request.POST or None, instance=cliente)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('clientes')
        return render(request, 'viajens/criar_clientes.html', {'form': form, 'editando': True})
    
def criar_onibus_view(request):
    form = forms.OnibusForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('onibus')
    return render(request, 'viajens/criar_onibus.html', {'form': form})

def onibus_view(request):
    try:
        onibus = Onibus.objects.all()
    except:
        onibus = None
    context = {'onibus': onibus}
    HTTP_STRING = render(request, 'viajens/onibus.html',context=context)
    return HttpResponse(HTTP_STRING)

def editar_onibus_view(request,id = None):
    if id is not None:
        onibus = get_object_or_404(Onibus, id=id)
        form = forms.OnibusForm(request.POST or None, instance=onibus)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return redirect('onibus')
        return render(request, 'viajens/criar_onibus.html', {'form': form, 'editando': True})
    
def viagem_view(request):
    if request.method == "POST":
        for chave, valor in request.POST.items():
            if chave.startswith('viagem_'):
                viagem_id = chave.split('_')[1]
                novo_onibus_id = valor
                viagem = ViagemCliente.objects.get(id=viagem_id)

                if novo_onibus_id == "":
                    if viagem.onibus is not None:
                        viagem.onibus = None
                        viagem._change_reason = "Removido do ônibus para fila de espera"
                        viagem.save()
                else:
                    if viagem.onibus is None or str(viagem.onibus.id) != novo_onibus_id:
                        novo_onibus = Onibus.objects.get(id=novo_onibus_id)
                        viagem.onibus = novo_onibus
                        viagem._change_reason = "Alteração de ônibus em lote via painel"
                        viagem.save()
        return redirect('/viagem')
    
    hoje = date.today()
    todas_viagens_do_dia = ViagemCliente.objects.filter(data=hoje, status='Ativo').select_related('onibus')
    todos_onibus = Onibus.objects.all()
    viagens_por_placa = {}
    fila_de_espera = []
    for viagem in todas_viagens_do_dia:
        
        if viagem.onibus is None:
            fila_de_espera.append(viagem)
        else:
            placa = viagem.onibus.placa
            if placa not in viagens_por_placa:
                viagens_por_placa[placa] = {'numero' : viagem.onibus.numero,'capacidade': viagem.onibus.capacidade,'clientes':[]}
            if viagem.status == "Ativo":
                viagens_por_placa[placa]['clientes'].append(viagem)


    context = {
        'viagens': viagens_por_placa,
        'data_hoje': hoje,
        'todos_onibus': todos_onibus,
        'fila_de_espera': fila_de_espera
    }
    return render(request, 'viajens/viagem.html', context)

def validar_viagem(request):
    if request.method == "POST":
        hora_atual = timezone.localtime().time()
        hora_limite = time(21, 30)
        hoje = date.today()
        agora_completo = timezone.now()
        
        onibus_lotados = Onibus.objects.filter(
            viagemcliente__data=hoje,
            viagemcliente__status='Ativo'
        ).annotate(
            total_passageiros=Count('viagemcliente')
        ).filter(
            total_passageiros__gt=F('capacidade')
        )


        if hora_atual < hora_limite:
            return render(request, 'viajens/snippets/alerta_erro.html', {'mensagem': f'Horario minimo de confirmaçao de viagem definido para {hora_limite}'})

        if onibus_lotados.exists():
            detalhes = [f"{o.numero} ({o.total_passageiros}/{o.capacidade})" for o in onibus_lotados]
            mensagem = f"Erro ao confirmar viagem, ônibus lotado: {', '.join(detalhes)}."
            
            return render(request, 'viajens/snippets/alerta_erro.html', {'mensagem': mensagem})

        #se tuod der certo o codigo chega aqui
        Viagem.objects.update_or_create(
            data=hoje,
            defaults={
                'status': 'Confirmada',
                'hora_de_confirmacao': agora_completo
            }
        )
        return render(request, 'viajens/snippets/alerta_sucesso.html', {'mensagem': "Viagem confirmada com sucesso!"})