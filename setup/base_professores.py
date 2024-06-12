from gestaoacademica.models import Professor
from django.contrib.auth import get_user_model


UserModel = get_user_model()

vendramel = Professor()
vendramel.user = UserModel.objects.filter(email="wvendramel@ifsp.edu.br")[0]
vendramel.nome = vendramel.user.first_name
vendramel.sobrenome = vendramel.user.last_name
vendramel.save()

andre = Professor()
andre.user = UserModel.objects.filter(email="andre.m.leme@ifsp.edu.br")[0]
andre.nome = andre.user.first_name
andre.sobrenome = andre.user.last_name
andre.save()

rosalvo = Professor()
rosalvo.user = UserModel.objects.filter(email="rosalvo@ifsp.edu.br")[0]
rosalvo.nome = rosalvo.user.first_name
rosalvo.sobrenome = rosalvo.user.last_name
rosalvo.save()

flavio = Professor()
flavio.user = UserModel.objects.filter(email="amate@ifsp.edu.br")[0]
flavio.nome = flavio.user.first_name
flavio.sobrenome = flavio.user.last_name
flavio.save()
