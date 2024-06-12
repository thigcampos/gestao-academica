from django.contrib.auth import get_user_model
from django.utils import timezone

UserModel = get_user_model()

# Alunos

if not UserModel.objects.filter(email='thi@gmail.com').exists():
    user=UserModel.objects.create_user(email="thi@gmail.com", password="123")
    user.date_joined= timezone.now()
    user.first_name = "Thiago"
    user.last_name = "Campos"
    user.is_superuser=False
    user.is_staff=True
    user.save()

if not UserModel.objects.filter(email='pri@gmail.com').exists():
    user=UserModel.objects.create_user(email="pri@gmail.com", password="123")
    user.date_joined= timezone.now()
    user.first_name = "Priscila"
    user.last_name = "Santana"
    user.is_superuser=False
    user.is_staff=True
    user.save()

if not UserModel.objects.filter(email='matheushpr9@gmail.com').exists():
    user=UserModel.objects.create_user(email="matheushpr9@gmail.com", password="123")
    user.date_joined= timezone.now()
    user.first_name = "Matheus Henrique"
    user.last_name = "Ptasinski Rosa"
    user.is_superuser=False
    user.is_staff=True
    user.save()

# Professores

if not UserModel.objects.filter(email='wvendramel@ifsp.edu.br').exists():
    user=UserModel.objects.create_user(email="wvendramel@ifsp.edu.br", password="123")
    user.date_joined= timezone.now()
    user.first_name = "Wilson"
    user.last_name = "Vendramel"
    user.is_superuser=True
    user.is_staff=True
    user.save()

if not UserModel.objects.filter(email='andre.m.leme@ifsp.edu.br').exists():
    user=UserModel.objects.create_user(email="andre.m.leme@ifsp.edu.br", password="123")
    user.date_joined= timezone.now()
    user.first_name = "André"
    user.last_name = "Leme"
    user.is_superuser=True
    user.is_staff=True
    user.save()

if not UserModel.objects.filter(email='rosalvo@ifsp.edu.br').exists():
    user=UserModel.objects.create_user(email="rosalvo@ifsp.edu.br", password="123")
    user.date_joined= timezone.now()
    user.first_name = "Rosalvo"
    user.last_name = "Filho"
    user.is_superuser=True
    user.is_staff=True
    user.save()

if not UserModel.objects.filter(email='amate@ifsp.edu.br').exists():
    user=UserModel.objects.create_user(email="amate@ifsp.edu.br", password="123")
    user.date_joined= timezone.now()
    user.first_name = "Flávio"
    user.last_name = "Amate"
    user.is_superuser=True
    user.is_staff=True
    user.save()