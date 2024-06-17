from gestaoacademica.models import OfertaDisciplina, Disciplina, Turma, Professor, Sala
from django.contrib.auth import get_user_model
import datetime

UserModel = get_user_model()

redI = OfertaDisciplina()
redI.professor = Professor.objects.all().filter(nome="Rosalvo")[0]
redI.disciplina = Disciplina.objects.all().filter(nome="Redes I")[0]
redI.diaDaSemana = "SEGUNDA"
redI.sala = Sala.objects.all().filter(idSala="A405")[0]
redI.horarioInicio = datetime.time(hour=19, minute=0, second=0)
redI.horarioFim = datetime.time(hour=22, minute=30, second=0)

turmaRedI = Turma()
turmaRedI.nome = f"{redI.disciplina.nome} ({redI.professor.nome}) {redI.diaDaSemana} {redI.horarioInicio} - {redI.horarioFim}"
turmaRedI.save()
redI.turma = Turma.objects.all().filter(nome=turmaRedI.nome)[0]
redI.save()

redII = OfertaDisciplina()
redII.professor = Professor.objects.all().filter(nome="Flávio")[0]
redII.disciplina = Disciplina.objects.all().filter(nome="Redes II")[0]
redII.diaDaSemana = "TERCA"
redII.sala = Sala.objects.all().filter(idSala="B406")[0]
redII.horarioInicio = datetime.time(hour=19, minute=0, second=0)
redII.horarioFim = datetime.time(hour=22, minute=30, second=0)

turmaRedII = Turma()
turmaRedII.nome = f"{redII.disciplina.nome} ({redII.professor.nome}) {redII.diaDaSemana} {redII.horarioInicio} - {redII.horarioFim}"
turmaRedII.save()
redII.turma = Turma.objects.all().filter(nome=turmaRedII.nome)[0]
redII.save()

eng = OfertaDisciplina()
eng.professor = Professor.objects.all().filter(nome="Wilson")[0]
eng.disciplina = Disciplina.objects.all().filter(nome="Engenharia de Software")[0]
eng.diaDaSemana = "TERCA"
eng.sala = Sala.objects.all().filter(idSala="B508")[0]
eng.horarioInicio = datetime.time(hour=19, minute=0, second=0)
eng.horarioFim = datetime.time(hour=22, minute=30, second=0)

turmaEng = Turma()
turmaEng.nome = f"{eng.disciplina.nome} ({eng.professor.nome}) {eng.diaDaSemana} {eng.horarioInicio} - {eng.horarioFim}"
turmaEng.save()
eng.turma = Turma.objects.all().filter(nome=turmaEng.nome)[0]
eng.save()


qua = OfertaDisciplina()
qua.professor = Professor.objects.all().filter(nome="Wilson")[0]
qua.disciplina = Disciplina.objects.all().filter(nome="Qualidade de Software")[0]
qua.diaDaSemana = "QUARTA"
qua.sala = Sala.objects.all().filter(idSala="B508")[0]
qua.horarioInicio = datetime.time(hour=19, minute=0, second=0)
qua.horarioFim = datetime.time(hour=22, minute=30, second=0)

turmaQua = Turma()
turmaQua.nome = f"{qua.disciplina.nome} ({qua.professor.nome}) {qua.diaDaSemana} {qua.horarioInicio} - {qua.horarioFim}"
turmaQua.save()
qua.turma = Turma.objects.all().filter(nome=turmaQua.nome)[0]
qua.save()


gpr = OfertaDisciplina()
gpr.professor = Professor.objects.all().filter(nome="André")[0]
gpr.disciplina = Disciplina.objects.all().filter(nome="Gestão de Projetos")[0]
gpr.diaDaSemana = "QUINTA"
gpr.sala = Sala.objects.all().filter(idSala="A405")[0]
gpr.horarioInicio = datetime.time(hour=19, minute=0, second=0)
gpr.horarioFim = datetime.time(hour=20, minute=40, second=0)

turmaGpr = Turma()
turmaGpr.nome = f"{gpr.disciplina.nome} ({gpr.professor.nome}) {gpr.diaDaSemana} {gpr.horarioInicio} - {gpr.horarioFim}"
turmaGpr.save()
gpr.turma = Turma.objects.all().filter(nome=turmaGpr.nome)[0]
gpr.save()

sip = OfertaDisciplina()
sip.professor = Professor.objects.all().filter(nome="Rosalvo")[0]
sip.disciplina = Disciplina.objects.all().filter(nome="Sistemas Operacionais")[0]
sip.diaDaSemana = "SEXTA"
sip.sala = Sala.objects.all().filter(idSala="A501")[0]
sip.horarioInicio = datetime.time(hour=19, minute=0, second=0)
sip.horarioFim = datetime.time(hour=22, minute=30, second=0)

turmaSip = Turma()
turmaSip.nome = f"{sip.disciplina.nome} ({sip.professor.nome}) {sip.diaDaSemana} {sip.horarioInicio} - {sip.horarioFim}"
turmaSip.save()
sip.turma = Turma.objects.all().filter(nome=turmaSip.nome)[0]
sip.save()


bdI = OfertaDisciplina()
bdI.professor = Professor.objects.all().filter(nome="André")[0]
bdI.disciplina = Disciplina.objects.all().filter(nome="Banco de Dados I")[0]
bdI.diaDaSemana = "SEXTA"
bdI.sala = Sala.objects.all().filter(idSala="A405")[0]
bdI.horarioInicio = datetime.time(hour=19, minute=0, second=0)
bdI.horarioFim = datetime.time(hour=20, minute=40, second=0)

turmaBdI = Turma()
turmaBdI.nome = f"{bdI.disciplina.nome} ({bdI.professor.nome}) {bdI.diaDaSemana} {bdI.horarioInicio} - {bdI.horarioFim}"
turmaBdI.save()
bdI.turma = Turma.objects.all().filter(nome=turmaBdI.nome)[0]
bdI.save()

lpI = OfertaDisciplina()
lpI.professor = Professor.objects.all().filter(nome="Flávio")[0]
lpI.disciplina = Disciplina.objects.all().filter(nome="Lógica de Programação I")[0]
lpI.diaDaSemana = "SEXTA"
lpI.sala = Sala.objects.all().filter(idSala="B406")[0]
lpI.horarioInicio = datetime.time(hour=19, minute=0, second=0)
lpI.horarioFim = datetime.time(hour=22, minute=30, second=0)

turmaLpI = Turma()
turmaLpI.nome = f"{lpI.disciplina.nome} ({lpI.professor.nome}) {lpI.diaDaSemana} {lpI.horarioInicio} - {lpI.horarioFim}"
turmaLpI.save()
lpI.turma = Turma.objects.all().filter(nome=turmaLpI.nome)[0]
lpI.save()