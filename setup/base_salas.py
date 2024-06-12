from gestaoacademica.models import Sala
from django.contrib.auth import get_user_model


UserModel = get_user_model()
if len(Sala.objects.all().filter(idSala="A405")) == 0:
    salaA405 = Sala()
    salaA405.idSala = "A405"
    salaA405.capacidade = 0
    salaA405.save()

if len(Sala.objects.all().filter(idSala="B406")) == 0:
    salaB406 = Sala()
    salaB406.idSala = "B406"
    salaB406.capacidade = 40
    salaB406.save()

if len(Sala.objects.all().filter(idSala="B508")) == 0:
    salaB508 = Sala()
    salaB508.idSala = "B508"
    salaB508.capacidade = 40
    salaB508.save()

if len(Sala.objects.all().filter(idSala="A501")) == 0:
    salaA501 = Sala()
    salaA501.idSala = "A501"
    salaA501.capacidade = 40
    salaA501.save()
