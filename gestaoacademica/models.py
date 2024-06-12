from django.db import models
from django.conf import settings
import datetime

class Aluno(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.TextField(verbose_name="Nome do Aluno")
    sobrenome = models.TextField(verbose_name="Sobrenome do Aluno")
    registroAluno = models.IntegerField(db_index=True, unique=True, verbose_name="Registro do Aluno")


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
    cargaHoraria = models.FloatField(default=0.0)
    numeroDeaulas = models.SmallIntegerField(default=0)  
    dependencia = models.ForeignKey('self', on_delete = models.SET_NULL,null=True)
    
    def __str__(self) -> str:
        return self.nome



class Turma(models.Model):
    aluno = models.ManyToManyField(Aluno)
    nome = models.TextField()

class Professor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.TextField()

class Sala(models.Model):
    idSala = models.TextField()
    capacidade = models.SmallIntegerField(default=0)


class OfertaDisciplina(models.Model):
    DIAS_DA_SEMANA =[
        ("DOMINGO","Domingo"),
        ("SEGUNDA","Segunda-feira"),
        ("TERCA", "Terça-feira"),
        ("QUARTA", "Quarta-feira"),
        ("QUINTA", "Quinta-feira"),
        ("SEXTA", "Sexta-feira"),
        ("SABADO", "Sábado"),
    ]
    turma = models.ForeignKey(Turma, null=True, on_delete=models.SET_NULL)
    Professor = models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL)
    disciplina =models.ForeignKey(Disciplina, null=True, on_delete=models.SET_NULL)
    sala = models.ForeignKey(Sala, null=True, on_delete=models.SET_NULL) 
    diaDaSemana = models.TextField(choices=DIAS_DA_SEMANA)
    horarioInicio = models.TimeField(default=datetime.datetime.now().time())
    horarioFim = models.TimeField(default=datetime.datetime.now().time())

class Participacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    ofertaDisciplina = models.ForeignKey(OfertaDisciplina, on_delete=models.SET_NULL, null=True)