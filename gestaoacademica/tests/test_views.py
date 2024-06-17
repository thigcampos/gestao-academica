from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from http import HTTPStatus
from model_bakery.baker import (
    make,
)  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes

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
    ListaDeEspera,
)


class TestAlunoCreateView(TestCase):
    def setUp(self):
        self._url = reverse("alunos_create")

    def test_aluno_create_view_context(self):
        # Teste para verificar se o formulário de criação de usuário está presente no contexto
        response = self.client.get(self._url)
        assert response.context_data.get("user_creation_form") == UserCreationForm

    def test_aluno_create_view_post(self):
        # Teste para verificar a criação de um novo aluno
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
        assert User.objects.filter(email=post_data.get("email")).exists()
        assert Aluno.objects.filter(prontuario=post_data.get("prontuario")).exists()


class TestOfertaDisciplinaListView(TestCase):
    def setUp(self):
        self.url = reverse("oferta_disciplina_list")
        self.client.force_login(
            User.objects.get_or_create(email="testuser@mail.com")[0]
        )

    def test_get_list_of_oferta_disciplina(self):
        # Teste para verificar se a lista de ofertas de disciplinas é retornada corretamente
        oferta_disciplina = make(
            OfertaDisciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        response = self.client.get(self.url)
        oferta_disciplina_list = response.context["object_list"]
        assert list(oferta_disciplina_list) == [oferta_disciplina]


class TestParticipacaoCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.aluno = Aluno.objects.create(user=self.user)

    def test_successful_enrollment(self):
        # Teste para verificar a inscrição bem-sucedida em uma disciplina
        turma = make(
            Turma, aluno=[]
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        for index in range(1, 11):
            aluno = make(
                Aluno, prontuario=index
            )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            turma.aluno.add(aluno)
        professor = make(
            Professor
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        disciplina = make(
            Disciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        sala = make(
            Sala
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_disciplina = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
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
        assert response.status_code == 302
        assert response.url == reverse("home_page")
        assert Participacao.objects.filter(aluno=self.aluno).count() == 1

    def test_exceeded_credits_error(self):
        # Teste para verificar erro ao exceder o limite de créditos
        make(
            Participacao, aluno=self.aluno, _quantity=3
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_disciplina = make(
            OfertaDisciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_ids = [oferta_disciplina.pk]
        self.client.login(email="testuser@mail.com", password="secret")
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )
        assert response.status_code == 302
        assert response.url == reverse("oferta_disciplina_list")
        assert Participacao.objects.filter(aluno=self.aluno).count() == 3
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Créditos excedidos, máximo 20 (cada inscrição vale 5 créditos)"
        )

    def test_exceeded_credits_error_too_many_disciplinas(self):
        # Teste para verificar erro ao exceder o limite de créditos na criação da participação
        ofertas_disciplinas = make(
            OfertaDisciplina, _quantity=5
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_ids = [
            ofertas_disciplinas[0].pk,
            ofertas_disciplinas[1].pk,
            ofertas_disciplinas[2].pk,
            ofertas_disciplinas[3].pk,
            ofertas_disciplinas[4].pk,
        ]

        self.client.login(email="testuser@mail.com", password="secret")

        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )
        assert response.status_code == 302
        assert response.url == reverse("oferta_disciplina_list")
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Créditos excedidos, máximo 20 (cada inscrição vale 5 créditos)"
        )

    def test_dependecies_not_done(self):
        # Teste para verificar erro ao tentar inscrever-se em uma disciplina com dependência não realizada
        professor = make(
            Professor
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        primary_disciplina = make(
            Disciplina, nome="Dependencia"
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        secondary_disciplina = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            Disciplina, dependencia=primary_disciplina, nome="Disciplina"
        )
        oferta_disciplina = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            OfertaDisciplina, disciplina=secondary_disciplina, professor=professor
        )
        oferta_ids = [oferta_disciplina.pk]
        dependencia = Disciplina.objects.filter(
            nome=oferta_disciplina.disciplina.dependencia.nome
        ).first()

        self.client.login(email="testuser@mail.com", password="secret")
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )

        assert response.status_code == 302
        assert response.url == reverse("oferta_disciplina_list")
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == f"A disciplina {oferta_disciplina.disciplina.nome} tem como pré-requisito {dependencia.nome}, a qual você não cursou"
        )

    def test_schedule_conflict_error(self):
        # Teste para verificar erro de conflito de horários
        turma = make(
            Turma, aluno=[]
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        turma.aluno.add(self.aluno)
        professor = make(
            Professor
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        disciplina = make(
            Disciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        sala = make(
            Sala, capacidade=10
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_disciplina1 = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            OfertaDisciplina,
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            sala=sala,
        )
        oferta_disciplina2 = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            OfertaDisciplina,
            turma=turma,
            disciplina=disciplina,
            professor=professor,
            sala=sala,
        )
        make(
            Participacao, aluno=self.aluno, ofertaDisciplina=oferta_disciplina2
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_ids = [oferta_disciplina1.pk]
        self.client.login(email="testuser@mail.com", password="secret")
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )
        assert response.status_code == 302
        assert response.url == reverse("oferta_disciplina_list")
        assert Participacao.objects.count() == 1
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Há conflito de horários"
        )

    def test_room_capacity_error(self):
        # Teste para verificar erro ao exceder a capacidade da sala
        turma = make(
            Turma, aluno=[]
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        turma.aluno.add(self.aluno)
        professor = make(
            Professor
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        disciplina = make(
            Disciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        sala = make(
            Sala, capacidade=1
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_disciplina = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
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
        assert response.status_code == 302
        assert response.url == reverse("oferta_disciplina_list")


class TestAlunoDisciplinaListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.aluno = Aluno.objects.create(user=self.user)

    def test_authenticated_user_view(self):
        # Teste para verificar o acesso à visualização para um usuário autenticado
        self.client.login(email="testuser@mail.com", password="secret")
        response = self.client.get(reverse("aluno_disciplina_list"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "alunos/list.html")

    def test_view_with_participations(self):
        # Teste para verificar a visualização com participações existentes
        oferta_disciplina1 = make(
            OfertaDisciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        oferta_disciplina2 = make(
            OfertaDisciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        make(
            Participacao, aluno=self.aluno, ofertaDisciplina=oferta_disciplina1
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        make(
            Participacao, aluno=self.aluno, ofertaDisciplina=oferta_disciplina2
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        self.client.login(email="testuser@mail.com", password="secret")
        response = self.client.get(reverse("aluno_disciplina_list"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "alunos/list.html")
        assert response.context["object_list"] == [
            oferta_disciplina1,
            oferta_disciplina2,
        ]


class TestOtherParticipacaoCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.client.login(email=self.user.email, password="secret")

    def test_remove_disciplina_pendente(self):
        disciplina_pendente = "Test Disciplina (some additional info)"
        session = self.client.session
        session["disciplinas_pendentes"] = [disciplina_pendente]
        session.save()

        post_data = {"disciplina-pendente": [disciplina_pendente]}
        response = self.client.post(
            reverse("other_participacao_create"), data=post_data
        )

        assert response.status_code == 302
        assert reverse("oferta_disciplina_list") == response.url
        assert "disciplinas_pendentes" in self.client.session
        assert len(self.client.session["disciplinas_pendentes"]) == 0


class TestListaDeEsperaCreateView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.aluno = Aluno.objects.create(user=self.user)
        self.professor = make(
            Professor
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        self.disciplina = make(
            Disciplina, nome="Test Disciplina"
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        self.oferta_disciplina = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            OfertaDisciplina, disciplina=self.disciplina, professor=self.professor
        )
        self.client.login(email=self.user.email, password="secret")

    def test_create_lista_de_espera(self):
        # Teste da criação da lista de espera
        disciplina_pendente = f"{self.disciplina.nome}"
        session = self.client.session
        session["disciplinas_pendentes"] = [disciplina_pendente]
        session.save()

        post_data = {"disciplina-pendente": [disciplina_pendente]}
        response = self.client.post(reverse("lista_espera_create"), data=post_data)

        assert response.status_code == 302
        assert response.url == reverse("oferta_disciplina_list")
        assert "disciplinas_pendentes" in self.client.session
        assert len(self.client.session["disciplinas_pendentes"]) == 0
        assert ListaDeEspera.objects.filter(
            ofertaDisciplina=self.oferta_disciplina, aluno=self.aluno
        ).exists()
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Aluno inserido na lista de espera!"
        )
        assert "lista_de_espera" in self.client.session
        assert str(self.oferta_disciplina) in self.client.session["lista_de_espera"]

    def test_create_lista_de_espera_on_a_row(self):
        # Teste da criação da lista de espera em sequência
        disciplina_pendente = f"{self.disciplina.nome}"
        session = self.client.session
        session["lista_de_espera"] = []
        session["disciplinas_pendentes"] = [disciplina_pendente]
        session.save()

        post_data = {"disciplina-pendente": [disciplina_pendente]}
        response = self.client.post(reverse("lista_espera_create"), data=post_data)

        assert response.status_code == 302
        assert response.url == reverse("oferta_disciplina_list")
        assert "disciplinas_pendentes" in self.client.session
        assert len(self.client.session["disciplinas_pendentes"]) == 0
        assert ListaDeEspera.objects.filter(
            ofertaDisciplina=self.oferta_disciplina, aluno=self.aluno
        ).exists()
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Aluno inserido na lista de espera!"
        )
        assert "lista_de_espera" in self.client.session
        assert str(self.oferta_disciplina) in self.client.session["lista_de_espera"]


class TestParticipacaoDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.aluno = Aluno.objects.create(user=self.user)
        self.disciplina = make(
            Disciplina, nome="Test Disciplina"
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        self.oferta_disciplina = make(
            OfertaDisciplina, disciplina=self.disciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        self.participacao = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            Participacao, ofertaDisciplina=self.oferta_disciplina, aluno=self.aluno
        )

    def test_successful_delete_participacao(self):
        self.client.login(email="testuser@mail.com", password="secret")

        post_data = {"disciplina-solicitada": [self.disciplina.nome]}
        response = self.client.post(reverse("participacao_delete"), data=post_data)

        assert response.status_code == 302
        assert reverse("aluno_disciplina_list") == response.url
        assert (
            Participacao.objects.filter(
                aluno=self.aluno, ofertaDisciplina=self.oferta_disciplina
            ).count()
            == 0
        )
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Inscrição cancelada com sucesso!"
        )


class TestListaDeEsperaDeleteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="secret"
        )
        self.aluno = Aluno.objects.create(user=self.user)
        self.disciplina = make(
            Disciplina, nome="Test Disciplina"
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        self.oferta_disciplina = make(
            OfertaDisciplina, disciplina=self.disciplina
        )  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
        self.lista_de_espera = make(  # Model Bakery nos permite criar uma instância persistente da classe e mantê-la até o fim dos testes
            ListaDeEspera, ofertaDisciplina=self.oferta_disciplina, aluno=[self.aluno]
        )

    def test_successful_delete_lista_de_espera(self):
        self.client.login(email="testuser@mail.com", password="secret")

        disciplina_solicitada = f"{self.disciplina.nome}"
        session = self.client.session
        session["lista_de_espera"] = [disciplina_solicitada]
        session.save()

        post_data = {"disciplina-solicitada": [disciplina_solicitada]}
        response = self.client.post(reverse("lista_espera_delete"), data=post_data)

        assert response.status_code == 302
        assert reverse("aluno_disciplina_list") == response.url
        assert (
            ListaDeEspera.objects.filter(
                aluno=self.aluno, ofertaDisciplina=self.oferta_disciplina
            ).count()
            == 0
        )
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Inscrição na lista de espera cancelada com sucesso!"
        )
        assert "lista_de_espera" in self.client.session
        assert len(self.client.session["lista_de_espera"]) == 0
