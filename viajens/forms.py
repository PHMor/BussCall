from django import forms
from viajens.models import Cliente
from viajens.models import Onibus

def validar_cpf(cpf):
    c = [int(d) for d in str(cpf) if d.isdigit()]
    
    if len(c) != 11 or len(set(c)) == 1: 
        return False
    
    d1 = (sum(c[i] * (10 - i) for i in range(9)) * 10 % 11) % 10
    d2 = (sum(c[i] * (11 - i) for i in range(10)) * 10 % 11) % 10
    
    return c[9] == d1 and c[10] == d2

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'cpf','onibus']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 11988887777',
                'maxlength': '15'
            }),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'onibus': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['onibus'].empty_label = "Nenhum"
        if self.instance and self.instance.pk:
            telefone_db = self.instance.telefone
            if telefone_db and telefone_db.startswith('55'):
                self.initial['telefone'] = telefone_db[2:]

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        
        if not validar_cpf(cpf):
            raise forms.ValidationError("Este CPF é inválido.")
        
        if Cliente.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este CPF já pertence a outro cliente.")
            
        return cpf
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        
        apenas_numeros = "".join(filter(str.isdigit, str(telefone)))

        if len(apenas_numeros) not in [10, 11]:
            raise forms.ValidationError("O telefone deve conter o DDD e o número (10 ou 11 dígitos).")

        if len(apenas_numeros) == 10:
            ddd = apenas_numeros[:2]
            resto = apenas_numeros[2:]
            apenas_numeros = f"{ddd}9{resto}"

        telefone_final = f"55{apenas_numeros}"

        if Cliente.objects.filter(telefone=telefone_final).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este número de telefone já está cadastrado.")

        return telefone_final
        
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        c = [int(d) for d in str(nome) if d.isdigit()]
        if len(c) > 0 or len(nome.split()) < 2:
            raise forms.ValidationError("Este nome é inválido.")
        return nome
    
class OnibusForm(forms.ModelForm):
    class Meta:
        model = Onibus
        fields = ['placa','numero','capacidade']

    def clean_placa(self):
        placa = self.cleaned_data.get('placa')
        return placa
    
    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        return numero