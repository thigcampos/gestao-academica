from gestaoacademica.models import Aluno
from django.contrib.auth import get_user_model
import datetime

UserModel = get_user_model()

thi = Aluno()
thi.user = UserModel.objects.filter(email='thi@gmail.com')[0]
thi.nome = thi.user.first_name
thi.sobrenome = thi.user.last_name
thi.save()