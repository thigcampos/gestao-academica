from django.contrib import admin
from gestaoacademica.models import Aluno, Disciplina, Participacao, Turma, Professor, OfertaDisciplina

@admin.register(Aluno, Disciplina, Participacao, Turma, Professor, OfertaDisciplina)
class PersonAdmin(admin.ModelAdmin):
    pass