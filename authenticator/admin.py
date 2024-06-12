from django.contrib import admin
from gestaoacademica.models import (
    Aluno,
    Disciplina,
    Participacao,
    Turma,
    Professor,
    OfertaDisciplina,
    Sala,
    ListaDeEspera,
)


@admin.register(
    Aluno, Disciplina, Participacao, Turma, Professor, OfertaDisciplina, Sala,ListaDeEspera
)
class PersonAdmin(admin.ModelAdmin):
    pass
