from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus
from model_bakery.baker import make

from authenticator.forms import UserCreationForm
from authenticator.models import User
from gestaoacademica.models import (
    Aluno,
    OfertaDisciplina,
    Disciplina,
    Turma,
    Professor,
    Sala,
)


class TestAlunoCreateView(TestCase):
    def setUp(self):
        self._url = reverse("alunos_create")

    def test_aluno_create_view_context(self):
        response = self.client.get(self._url)
        assert response.context_data.get("user") == UserCreationForm

    def test_aluno_create_view_post(self):
        post_data = {
            "nome": "some_string",
            "sobrenome": "other_string",
            "prontuario": "another_string",
            "email": "testuser@mail.com",
            "password1": "foobar",
            "password2": "foobar",
        }
        response = self.client.post(self._url, data=post_data)

        assert response.status_code == HTTPStatus.FOUND
        assert User.objects.filter(email=post_data.get("email"))
        assert Aluno.objects.filter(prontuario=post_data.get("prontuario"))


class TestOfertaDisciplinaListView(TestCase):
    def setUp(self):
        self.url = reverse("oferta_disciplina_list")
        self.client.force_login(
            User.objects.get_or_create(email="testuser@mail.com")[0]
        )

    def test_get_list_of_oferta_disciplina(self):
        oferta_disciplina = make(OfertaDisciplina)
        response = self.client.get(self.url)
        oferta_disciplina_list = response.context["object_list"]
        assert list(oferta_disciplina_list) == [oferta_disciplina]


class TestParticipacaoCreateView(TestCase):
    def setUp(self):
        self._url = reverse("participacao_create")
        self.user = make(User)
        self.aluno = make(Aluno, user=self.user)
        self.client.force_login(User.objects.get_or_create(email=self.user.email)[0])

    def test_participacao_create_form(self):
        turma = make(Turma, aluno=[])
        for index in range(1, 11):
            aluno = make(Aluno, prontuario=index)
            turma.aluno.add(aluno)
        professor = make(Professor)
        disciplina = make(Disciplina)
        sala = make(Sala)
        oferta_disciplina = make(
            OfertaDisciplina,
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            sala=sala,
        )
        post_data = {"oferta-disciplina": [oferta_disciplina.id]}

        response = self.client.post(self._url, data=post_data)
        assert response.status_code == HTTPStatus.FOUND
