from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

class MembroEquipeInline(admin.TabularInline):
    model = MembroEquipe
    extra = 1

class JogoPlataformaInline(admin.TabularInline):
    model = Jogo_Plataforma
    extra = 1



class AlocacaoInline(admin.TabularInline):
    model = Alocacao
    extra = 1

class EtapaDesenvolvimentoInline(admin.TabularInline):
    model = EtapaDesenvolvimento
    extra = 1

class TarefaInline(admin.TabularInline):
    model = Tarefa
    extra = 1
    
class AssetDigitalInline(admin.TabularInline):
    model = AssetDigital
    extra = 1 
    
@admin.register(AssetDigital)
class AssetDigitalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'arquivo', 'versao', 'autor', 'jogo', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.arquivo and obj.arquivo.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return mark_safe(f'<img src="{obj.arquivo.url}" style="max-height: 150px; border-radius:20%">')
        return "Não é imagem ou não enviado"

    preview.short_description = 'Pré-visualização'


class EstudioDesenvolvimentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'site', 'telefone', 'cidade', 'email')
    search_fields = ('nome',)
    inlines = [MembroEquipeInline]

class JogoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'genero', 'data_lancamento', 'estudio')
    search_fields = ('titulo',)
    inlines = [JogoPlataformaInline, EtapaDesenvolvimentoInline, AssetDigitalInline, AlocacaoInline]

class CenarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'jogo', 'descricao_curta', 'arquivo_link')
    search_fields = ('nome', 'descricao')

    def descricao_curta(self, obj):
        if obj.descricao:
            return obj.descricao[:50] + '...' if len(obj.descricao) > 50 else obj.descricao
        return '-'
    descricao_curta.short_description = 'Descrição'

    def arquivo_link(self, obj):
        if obj.arquivo:
            return mark_safe(f'<a href="{obj.arquivo.url}" target="_blank">Download</a>')
        return '-'
    arquivo_link.short_description = 'Arquivo'

class MembroEquipeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'funcao', 'cidade', 'telefone', 'data_admissao')
    search_fields = ('nome', 'email')

admin.site.register(Funcao)
admin.site.register(TurnoTrabalho)
admin.site.register(TipoAnalise)
admin.site.register(Cidade)
admin.site.register(PlataformaJogo)
admin.site.register(EstudioDesenvolvimento, EstudioDesenvolvimentoAdmin)
admin.site.register(MembroEquipe, MembroEquipeAdmin)
admin.site.register(Jogo, JogoAdmin)
admin.site.register(EtapaDesenvolvimento)
admin.site.register(Tarefa)
admin.site.register(TarefaDetalhe)
admin.site.register(ComponenteProjetoJogo)
admin.site.register(Cenario, CenarioAdmin)
admin.site.register(Cenario_Asset)
admin.site.register(Ocorrencia)
admin.site.register(AnaliseProcesso)
admin.site.register(UsuarioSistema)
admin.site.register(ConfiguracaoSistema)
