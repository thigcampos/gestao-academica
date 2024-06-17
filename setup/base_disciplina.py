from gestaoacademica.models import Disciplina
from django.contrib.auth import get_user_model


UserModel = get_user_model()
if len(Disciplina.objects.all().filter(nome="Redes I")) == 0:
    redes1 = Disciplina()
    redes1.nome = "Redes I"
    redes1.cargaHoraria = 80
    redes1.save()

if len(Disciplina.objects.all().filter(nome="Redes II")) == 0:
    redes2 = Disciplina()
    redes2.nome = "Redes II"
    redes2.cargaHoraria = 80
    redes2.dependencia = Disciplina.objects.all().filter(nome="Redes I")[0]
    redes2.save()

if len(Disciplina.objects.all().filter(nome="Engenharia de Software")) == 0:
    eng = Disciplina()
    eng.nome = "Engenharia de Software"
    eng.cargaHoraria = 80
    eng.save()

if len(Disciplina.objects.all().filter(nome="Qualidade de Software")) == 0:
    qua = Disciplina()
    qua.nome = "Qualidade de Software"
    qua.cargaHoraria = 80
    qua.dependencia = Disciplina.objects.all().filter(nome="Engenharia de Software")[0]
    qua.save()

if len(Disciplina.objects.all().filter(nome="Gestão de Projetos")) == 0:
    gpr = Disciplina()
    gpr.nome = "Gestão de Projetos"
    gpr.cargaHoraria = 40
    gpr.save()

if len(Disciplina.objects.all().filter(nome="Sistemas Operacionais")) == 0:
    sip = Disciplina()
    sip.nome = "Sistemas Operacionais"
    sip.cargaHoraria = 80
    sip.save()

if len(Disciplina.objects.all().filter(nome="Banco de Dados I")) == 0:
    bdI = Disciplina()
    bdI.nome = "Banco de Dados I"
    bdI.cargaHoraria = 80
    bdI.save()

if len(Disciplina.objects.all().filter(nome="Lógica de Programação I")) == 0:
    lpI = Disciplina()
    lpI.nome = "Lógica de Programação I"
    lpI.cargaHoraria = 80
    lpI.save()

if len(Disciplina.objects.all().filter(nome="Sistemas Web I")) == 0:
    lpI = Disciplina()
    lpI.nome = "Sistemas Web I"
    lpI.cargaHoraria = 80
    lpI.save()
