from django.contrib import admin
from .models import *

# (i) Ocupação e Pessoas
class PessoaInline(admin.TabularInline):
    model = Pessoa
    extra = 1

class OcupacaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [PessoaInline]


# (ii) Instituição e Cursos
class CursoInline(admin.TabularInline):
    model = Curso
    extra = 1

class InstituicaoEnsinoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [CursoInline]


# (iii) Área do saber e Cursos
class CursoInlineArea(admin.TabularInline):
    model = Curso
    extra = 1

class AreaSaberAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)
    inlines = [CursoInlineArea]


# (iv) Cursos e Disciplinas (CursoDisciplina)
class CursoDisciplinaInline(admin.TabularInline):
    model = CursoDisciplina
    extra = 1

class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'instituicao', 'area_saber')
    search_fields = ('nome',)
    inlines = [CursoDisciplinaInline]


# (v) Disciplinas e Avaliações
class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 1

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'area_saber')
    search_fields = ('nome',)
    inlines = [AvaliacaoInline]


# Registro dos models no admin
admin.site.register(Cidade)
admin.site.register(Ocupacao, OcupacaoAdmin)
admin.site.register(Pessoa)
admin.site.register(InstituicaoEnsino, InstituicaoEnsinoAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(AreaSaber, AreaSaberAdmin)
admin.site.register(Turma)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(AvaliacaoTipo)
admin.site.register(Matricula)
admin.site.register(Avaliacao)
admin.site.register(Frequencia)
admin.site.register(Turno)
admin.site.register(Ocorrencia)
admin.site.register(CursoDisciplina)
