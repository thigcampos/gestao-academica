from http import HTTPStatus
from django.urls import resolve, reverse
from django.test import TestCase
from model_bakery.baker import make

from authenticator.models import User
from gestaoacademica.models import (
    Aluno,
    OfertaDisciplina,
    Turma,
    Sala,
    Disciplina,
    Professor,
)
from gestaoacademica.views import (
    HomePageView,
    LoginPageView,
    AlunoCreateView,
    OfertaDisciplinaListView,
    AlunoDisciplinaListView,
    ParticipacaoCreateView,
)


class TestRoutesLogin(TestCase):
    def setUp(self):
        self._url = reverse("accounts_login")

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == LoginPageView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "registration/login.html")


class TestRoutesHomePage(TestCase):
    def setUp(self):
        self._url = reverse("home_page")
        self.client.force_login(
            User.objects.get_or_create(email="testuser@mail.com")[0]
        )

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == HomePageView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "general/home.html")


class TestRoutesAlunosCreate(TestCase):
    def setUp(self):
        self._url = reverse("alunos_create")
        self.client.force_login(
            User.objects.get_or_create(email="testuser@mail.com")[0]
        )

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == AlunoCreateView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "alunos/create.html")


class TestRoutesOfertaDisciplinaList(TestCase):
    def setUp(self):
        self._url = reverse("oferta_disciplina_list")
        self.client.force_login(
            User.objects.get_or_create(email="testuser@mail.com")[0]
        )

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == OfertaDisciplinaListView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "disciplinas/list.html")


class TestRoutesParticipacaoCreate(TestCase):
    def setUp(self):
        self._url = reverse("participacao_create")
        self.user = make(User)
        self.aluno = make(Aluno, user=self.user)
        self.client.force_login(User.objects.get_or_create(email=self.user.email)[0])

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == ParticipacaoCreateView

    def test_loads_correct_view(self):
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


class TestRoutesAlunoDisciplinaList(TestCase):
    def setUp(self):
        self._url = reverse("aluno_disciplina_list")
        self.user = make(User)
        self.aluno = make(Aluno, user=self.user)
        self.client.force_login(User.objects.get_or_create(email=self.user.email)[0])

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == AlunoDisciplinaListView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "alunos/list.html")
