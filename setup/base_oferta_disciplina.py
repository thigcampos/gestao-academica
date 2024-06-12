from gestaoacademica.models import OfertaDisciplina, Disciplina, Turma, Professor, Sala
from django.contrib.auth import get_user_model
import datetime

UserModel = get_user_model()

redI = OfertaDisciplina()
redI.professor = Professor.objects.all().filter(nome = "Rosalvo")[0]
redI.disciplina = Disciplina.objects.all().filter(nome = "Redes I")[0]
redI.diaDaSemana = "SEGUNDA"
redI.sala = Sala.objects.all().filter(idSala = "A405")[0]
redI.horarioInicio = datetime.time(hour=19,minute=0,second=0)
redI.horarioFim = datetime.time(hour=22,minute=30,second=0)

turmaRedI = Turma()
turmaRedI.nome = "Redes I (Rosalvo) 19:00 - 22:00"
turmaRedI.save()
redI.turma = Turma.objects.all().filter(nome = "Redes I (Rosalvo) 19:00 - 22:00")[0]
redI.save()

redII = OfertaDisciplina()
redII.professor = Professor.objects.all().filter(nome = "Flávio")[0]
redII.disciplina = Disciplina.objects.all().filter(nome = "Redes II")[0]
redII.diaDaSemana = "TERCA"
redII.sala = Sala.objects.all().filter(idSala = "B406")[0]
redII.horarioInicio = datetime.time(hour=19,minute=0,second=0)
redII.horarioFim = datetime.time(hour=22,minute=30,second=0)

turmaRedII = Turma()
turmaRedII.nome = f"{redII.disciplina.nome} ({redII.professor.nome}) {redII.horarioInicio} - {redII.horarioFim}"
turmaRedII.save()
redII.turma = Turma.objects.all().filter(nome = turmaRedII.nome)[0]
redII.save()