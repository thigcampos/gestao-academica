from django.db import models
from django.conf import settings


class Aluno(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.TextField(verbose_name="Nome do Aluno")
    sobrenome = models.TextField(verbose_name="Sobrenome do Aluno")
    registroAluno = models.IntegerField(db_index=True, unique=True, verbose_name="Registro do Aluno")
    dataNascimento = models.DateTimeField(db_index=True, verbose_name="Data de Nascimento")

    matriculaStatus = models.BooleanField(default=False, verbose_name="Status da Matrícula")
    pagamentoStatus = models.BooleanField(default=False, verbose_name="Status do Pagamento")

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = "Aluno da Insituição"

    def __str__(self):
        return f"Aluno: {self.registroAluno}"


class Disciplina(models.Model):
    nome = models.TextField(verbose_name="Nome da Disciplina")


class Participacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
