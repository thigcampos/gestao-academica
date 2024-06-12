from gestaoacademica.models import Aluno
from django.contrib.auth import get_user_model


UserModel = get_user_model()
if len(Aluno.objects.all().filter(prontuario = "BP0000001")) == 0:
    thi = Aluno()
    thi.user = UserModel.objects.filter(email='thi@gmail.com')[0]
    thi.nome = thi.user.first_name
    thi.sobrenome = thi.user.last_name
    thi.prontuario = "BP0000001"
    thi.save()
if len(Aluno.objects.all().filter(prontuario = "BP0000002")) == 0:
    matheus = Aluno()
    matheus.user = UserModel.objects.filter(email='matheushpr9@gmail.com')[0]
    matheus.nome = matheus.user.first_name
    matheus.sobrenome = matheus.user.last_name
    matheus.prontuario = "BP0000002"
    matheus.save()
if len(Aluno.objects.all().filter(prontuario = "BP0000003")) == 0:
    pri = Aluno()
    pri.user = UserModel.objects.filter(email='pri@gmail.com')[0]
    pri.nome = pri.user.first_name
    pri.sobrenome = pri.user.last_name
    pri.prontuario = "BP0000003"
    pri.save()