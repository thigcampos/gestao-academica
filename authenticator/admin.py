from django.contrib import admin
from gestaoacademica.models import (
    Aluno,
    Disciplina,
    Participacao,
    Turma,
    Professor,
    OfertaDisciplina,
    Sala
)


@admin.register(Aluno, Disciplina, Participacao, Turma, Professor, OfertaDisciplina, Sala)
class PersonAdmin(admin.ModelAdmin):
    pass
