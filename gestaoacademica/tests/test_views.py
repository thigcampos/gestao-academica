from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

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
    Participacao,
)


class TestAlunoCreateView(TestCase):
    def setUp(self):
        self._url = reverse("alunos_create")

    def test_aluno_create_view_context(self):
        response = self.client.get(self._url)
        assert response.context_data.get("user_creation_form") == UserCreationForm

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


class ParticipacaoCreateViewTest(TestCase):
    """Unit tests for ParticipacaoCreateView"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.aluno = Aluno.objects.create(user=self.user)

    def test_successful_enrollment(self):
        """Test successful enrollment for a single course"""
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

        oferta_ids = [oferta_disciplina.pk]

        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )

        # Assert successful enrollment
        assert response.status_code == 302
        assert reverse("home_page") == response.url
        assert Participacao.objects.filter(aluno=self.aluno).count() == 1

    def test_exceeded_credits_error(self):
        """Test error handling for exceeding credit limit"""
        make(Participacao, aluno=self.aluno, _quantity=3)
        oferta_disciplina = make(OfertaDisciplina)
        oferta_ids = [oferta_disciplina.pk]

        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )

        # Assert error handling for exceeding credits
        assert response.status_code == 302
        assert reverse("oferta_disciplina_list") == response.url
        assert Participacao.objects.filter(aluno=self.aluno).count() == 3
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Créditos excedidos, máximo 3"
        )

    def test_exceeded_credits_error_on_creation(self):
        ofertas_disciplinas = make(OfertaDisciplina, _quantity=4)
        oferta_ids = [
            ofertas_disciplinas[0].pk,
            ofertas_disciplinas[1].pk,
            ofertas_disciplinas[2].pk,
            ofertas_disciplinas[3].pk,
        ]

        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )

        # Assert error handling for exceeding credits
        assert response.status_code == 302
        assert reverse("oferta_disciplina_list") == response.url
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Créditos excedidos, máximo 3"
        )

    def test_schedule_conflict_error(self):
        """Test error handling for schedule conflict"""
        turma = make(Turma, aluno=[])
        turma.aluno.add(self.aluno)
        professor = make(Professor)
        disciplina = make(Disciplina)
        sala = make(Sala, capacidade=10)
        oferta_disciplina1 = make(
            OfertaDisciplina,
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            sala=sala,
        )

        oferta_disciplina2 = make(
            OfertaDisciplina,
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            sala=sala,
        )

        oferta_ids = [oferta_disciplina1.pk, oferta_disciplina2.pk]

        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )

        # Assert error handling for schedule conflict
        assert response.status_code == 302
        assert reverse("oferta_disciplina_list") == response.url
        assert Participacao.objects.count() == 0  # No participations created
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Há conflito de horários"
        )

    def test_room_capacity_error(self):
        """Test error handling for room capacity limit"""
        turma = make(Turma, aluno=[])
        turma.aluno.add(self.aluno)
        professor = make(Professor)
        disciplina = make(Disciplina)
        sala = make(Sala, capacidade=1)
        oferta_disciplina = make(
            OfertaDisciplina,
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            sala=sala,
        )

        self.client.login(email="testuser@mail.com", password="secret")

        oferta_ids = [oferta_disciplina.pk]
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )

        print()
        # Assert error handling for room capacity
        assert response.status_code == 302
        assert reverse("oferta_disciplina_list") == response.url
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == f"Disciplina {oferta_disciplina.disciplina.nome} com capacidade máxima"
        )


class AlunoDisciplinaListViewTest(TestCase):
    """Unit tests for AlunoDisciplinaListView"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.aluno = Aluno.objects.create(user=self.user)

    def test_authenticated_user_view(self):
        """Test successful view access for an authenticated user"""
        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.get(reverse("aluno_disciplina_list"))

        assert response.status_code == 200
        self.assertTemplateUsed(response, "alunos/list.html")

    def test_view_with_participations(self):
        """Test view with existing participations"""
        oferta_disciplina1 = make(OfertaDisciplina)
        oferta_disciplina2 = make(OfertaDisciplina)

        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.get(reverse("aluno_disciplina_list"))

        assert response.status_code == 200
        self.assertTemplateUsed(response, "alunos/list.html")
        # Assert context data contains filtered OfertaDisciplina objects
        assert response.context["object_list"] == [
            oferta_disciplina1,
            oferta_disciplina2,
        ]

    def test_view_with_duplicates(self):
        """Test view handling duplicate participations for the same course"""
        oferta_disciplina = make(OfertaDisciplina)
        make(
            Participacao,
            aluno=self.aluno,
            ofertaDisciplina=oferta_disciplina,
            _quantity=2,
        )

        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.get(reverse("aluno_disciplina_list"))

        assert response.status_code == 200
        self.assertTemplateUsed(response, "alunos/list.html")
        # Assert context data contains only one OfertaDisciplina object
        assert len(response.context["object_list"]) == 1
        assert response.context["object_list"][0] == oferta_disciplina
