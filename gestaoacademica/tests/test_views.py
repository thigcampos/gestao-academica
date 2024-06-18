from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.messages import get_messages

from http import HTTPStatus
from model_bakery.baker import (
    make,
)

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
        oferta_disciplina = make(OfertaDisciplina)
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
        # Para tornar o teste o mais realista possível, criamos uma instância persistente de cada classe necessária
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
        # Após a criação da oferta da disciplina, montamos uma lista contendo o seu id
        oferta_ids = [oferta_disciplina.pk]
        # Realizamos o login
        self.client.login(email="testuser@mail.com", password="secret")
        # Realizamos a requisição
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )
        # Validamos se o sistema faz o redirect
        assert response.status_code == 302
        # Validamos se o usuário foi redirecionado para a tela inicial
        assert response.url == reverse("home_page")
        # Validamos se o usuário agora possui uma participacao
        assert Participacao.objects.filter(aluno=self.aluno).count() == 1

    def test_exceeded_credits_error(self):
        # Teste para verificar erro ao exceder o limite de créditos
        # Criação de 4 Participações vinculados ao aluno de teste (self.aluno) usando model_bakery
        make(Participacao, aluno=self.aluno, _quantity=4)
        oferta_disciplina = make(OfertaDisciplina)
        # Após a criação de uma oferta de disciplina, criamos uma lista contendo o id da oferta da disciplina
        # Utilizamos o ID da Oferta Disciplina e o Email do aluno (disponível no corpo da requisição do formulário) para validar as informações necessárias
        oferta_ids = [oferta_disciplina.pk]
        # Realizamos o login
        self.client.login(email="testuser@mail.com", password="secret")
        # Enviamos o formulário com o id da Oferta de Disciplina
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )

        # Validamos se o sistema faz o redirect (a listagem de ofertas de disciplina possui uma url diferente da criação de participações)
        assert response.status_code == 302
        # Validamos se o usuário foi redirecionado para "/disciplinas/", aqui identificada pelo nome "oferta_disciplina_list"
        assert response.url == reverse("oferta_disciplina_list")
        # Validamos se o aluno de teste possui 4 partipações (número máximo)
        assert Participacao.objects.filter(aluno=self.aluno).count() == 4
        # Validamos se a mensagem de erro foi exibida corretamente
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Créditos excedidos, máximo 20 (cada inscrição vale 5 créditos)"
        )

    def test_exceeded_credits_error_too_many_disciplinas(self):
        # Teste para verificar erro ao exceder o limite de créditos na criação da participação
        # Aqui, enviamos para o sistema 5 (25 créditos) inscrições ao mesmo tempo, número que excede o limite (4/20 créditos)
        ofertas_disciplinas = make(OfertaDisciplina, _quantity=5)
        # Após a criação de 5 ofertas de disciplinas, criamos uma lista com o Id de cada uma das ofertas
        oferta_ids = [
            ofertas_disciplinas[0].pk,
            ofertas_disciplinas[1].pk,
            ofertas_disciplinas[2].pk,
            ofertas_disciplinas[3].pk,
            ofertas_disciplinas[4].pk,
        ]

        # Realizamos o login
        self.client.login(email="testuser@mail.com", password="secret")
        # Fazemos o envio das informações
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )
        # Validamos se o sistema faz o redirect (a listagem de ofertas de disciplina possui uma url diferente da criação de participações)
        assert response.status_code == 302
        # Validamos se o usuário foi redirecionado para "/disciplinas/", aqui identificada pelo nome "oferta_disciplina_list"
        assert response.url == reverse("oferta_disciplina_list")
        # Validamos se a mensagem de erro foi exibida corretamente
        assert (
            str(list(get_messages(response.wsgi_request))[0])
            == "Créditos excedidos, máximo 20 (cada inscrição vale 5 créditos)"
        )

    def test_dependecies_not_done(self):
        # Teste para verificar erro ao tentar inscrever-se em uma disciplina com dependência não realizada
        professor = make(Professor)
        primary_disciplina = make(Disciplina, nome="Dependencia")
        secondary_disciplina = make(
            Disciplina, dependencia=primary_disciplina, nome="Disciplina"
        )
        oferta_disciplina = make(
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
        make(Participacao, aluno=self.aluno, ofertaDisciplina=oferta_disciplina2)
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
        # Criação de uma Sala com capacidade sendo 1 e para preenche-lá, há a criação do "other_aluno"
        other_aluno = make(Aluno, prontuario="BP300")
        turma = make(Turma, aluno=[])
        turma.aluno.add(other_aluno)
        # Criação de uma instância dos outro modelos que compõem OfertaDisciplina
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
        # Login com a conta do aluno de teste
        self.client.login(email="testuser@mail.com", password="secret")
        oferta_ids = [oferta_disciplina.pk]
        # Realização da requisição
        response = self.client.post(
            reverse("participacao_create"), {"oferta-disciplina": oferta_ids}
        )
        # Validação do redirecionamento do usuário para outra URL
        assert response.status_code == 302
        # Validação da URL atual do usuário, sendo esperado que esteja em /disciplinas/
        assert response.url == reverse("oferta_disciplina_list")
        # Validação de notificação ao usuário de disciplinas pendentes
        assert self.client.session["disciplinas_pendentes"] == [str(oferta_disciplina)]
        # No topo da listagem de ofertas de disciplina, o usuário é apresentado com duas opções, entrar na lista de espera ou inscrever-se em outra disciplina
        # Neste presente teste, optaremos pela segunda opção, por já existir um teste para a criação da lista de espera
        self.client.post(
            reverse("other_participacao_create"),
            {"disciplina-pendente": str(oferta_disciplina)},
        )
        # Validação do redirecionamento do usuário para outra URL
        assert response.status_code == 302
        # Validação da URL atual do usuário, sendo esperado que esteja em /disciplinas/
        assert response.url == reverse("oferta_disciplina_list")
        # Validação da lista de disciplinas pendentes, espera-se que esteja vazia
        assert self.client.session["disciplinas_pendentes"] == []


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
        oferta_disciplina1 = make(OfertaDisciplina)
        oferta_disciplina2 = make(OfertaDisciplina)
        make(Participacao, aluno=self.aluno, ofertaDisciplina=oferta_disciplina1)
        make(Participacao, aluno=self.aluno, ofertaDisciplina=oferta_disciplina2)
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
        self.professor = make(Professor)
        self.disciplina = make(Disciplina, nome="Test Disciplina")
        self.oferta_disciplina = make(
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
        self.disciplina = make(Disciplina, nome="Test Disciplina")
        self.oferta_disciplina = make(OfertaDisciplina, disciplina=self.disciplina)
        self.participacao = make(
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
        self.disciplina = make(Disciplina, nome="Test Disciplina")
        self.oferta_disciplina = make(OfertaDisciplina, disciplina=self.disciplina)
        self.lista_de_espera = make(
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
