from django import forms
from .models import *


class JogoForm(forms.ModelForm):
    class Meta:
        model = Jogo
        fields = ['titulo', 'genero', 'data_lancamento', 'estudio', 'descricao']


class EstudioDesenvolvimentoForm(forms.ModelForm):
    class Meta:
        model = EstudioDesenvolvimento
        fields = ['nome', 'site', 'telefone', 'cidade', 'email']


class PlataformaJogoForm(forms.ModelForm):
    class Meta:
        model = PlataformaJogo
        fields = ['nome']


class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidade
        fields = ['nome', 'uf']


class MembroEquipeForm(forms.ModelForm):
    class Meta:
        model = MembroEquipe
        fields = ['nome', 'email', 'funcao', 'cidade', 'telefone', 'data_admissao']


class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Funcao
        fields = ['nome']


class EtapaDesenvolvimentoForm(forms.ModelForm):
    class Meta:
        model = EtapaDesenvolvimento
        fields = ['nome', 'data_inicio', 'data_fim', 'jogo']


class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['descricao', 'prioridade', 'data_limite', 'etapa', 'responsavel']


class CenarioForm(forms.ModelForm):
    class Meta:
        model = Cenario
        fields = ['nome', 'descricao', 'jogo']

