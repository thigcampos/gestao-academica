from django.test import TestCase
from django.db.utils import IntegrityError
from model_bakery.baker import make
import datetime

from authenticator.models import User
from gestaoacademica.models import (
    Aluno,
    Professor,
    Turma,
    Sala,
    Disciplina,
    OfertaDisciplina,
)


class TestModelAluno(TestCase):
    def setUp(self):
        self.aluno = make(Aluno)

    def test_create_aluno(self):
        user = make(User)
        aluno_nome = "some_string"
        aluno_sobrenome = "other_string"
        aluno_prontuario = "another_string"
        aluno = Aluno.objects.create(
            user=user,
            nome=aluno_nome,
            sobrenome=aluno_sobrenome,
            prontuario=aluno_prontuario,
        )

        assert aluno.user == user
        assert aluno.nome == aluno_nome
        assert aluno.sobrenome == aluno_sobrenome
        assert aluno.prontuario == aluno_prontuario

    def test_prontuario_is_unique(self):
        with self.assertRaises(IntegrityError):
            other_aluno = make(Aluno, prontuario=self.aluno.prontuario)
            other_aluno.full_clean()

    def test_aluno_string_representation(self):
        assert str(self.aluno) == f"Aluno: {self.aluno.nome} {self.aluno.sobrenome}"


class TestModelTurma(TestCase):
    def setUp(self):
        self.aluno = make(Aluno)
        self.turma = make(Turma, aluno=[self.aluno])

    def test_create_turma(self):
        turma_nome = "some_string"
        turma = Turma.objects.create(nome=turma_nome)
        turma.aluno.set([self.aluno])

        assert turma.nome == turma_nome
        assert list(turma.aluno.all()) == [self.aluno]

    def test_turma_string_representation(self):
        assert str(self.turma) == self.turma.nome


class TestModelProfessor(TestCase):
    def setUp(self):
        self.professor = make(Professor)

    def test_create_aluno(self):
        user = make(User)
        professor_nome = "some_string"
        professor_sobrenome = "other_string"

        professor = Professor.objects.create(
            user=user, nome=professor_nome, sobrenome=professor_sobrenome
        )

        assert professor.user == user
        assert professor.nome == professor_nome
        assert professor_sobrenome == professor_sobrenome

    def test_professor_string_representation(self):
        assert (
            str(self.professor)
            == f"Professor: {self.professor.nome} {self.professor.sobrenome}"
        )


class TestModelSala(TestCase):
    def setUp(self):
        self.sala = make(Sala)

    def test_create_sala(self):
        sala_idSala = 500
        sala_capacidade = 40
        sala = Sala.objects.create(
            idSala=sala_idSala,
            capacidade=sala_capacidade,
        )

        assert sala.idSala == sala_idSala
        assert sala.capacidade == sala_capacidade

    def test_id_sala_is_unique(self):
        with self.assertRaises(IntegrityError):
            other_sala = make(Sala, idSala=self.sala.idSala)
            other_sala.full_clean()

    def test_sala_string_representation(self):
        assert str(self.sala) == self.sala.idSala


class TestModelDisciplina(TestCase):
    def setUp(self):
        self.disciplina = make(Disciplina)

    def test_create_disciplina(self):
        disciplina_nome = "some_string"
        disciplina_dependencia = make(Disciplina)
        disciplina_cargaHoraria = 50
        disciplina = Disciplina.objects.create(
            nome=disciplina_nome,
            dependencia=disciplina_dependencia,
            cargaHoraria=disciplina_cargaHoraria,
        )

        assert disciplina.nome == disciplina_nome
        assert disciplina.dependencia == disciplina_dependencia
        assert disciplina.cargaHoraria == disciplina_cargaHoraria

    def test_disciplina_string_representation(self):
        assert str(self.disciplina) == self.disciplina.nome


class TestModelOfertaDisciplina(TestCase):
    def setUp(self):
        self.turma = make(Turma)
        self.professor = make(Professor)
        self.disciplina = make(Disciplina)
        self.sala = make(Sala)
        self.ofertaDisciplina = make(
            OfertaDisciplina,
            turma=self.turma,
            professor=self.professor,
            disciplina=self.disciplina,
            sala=self.sala,
        )

    def test_create_disciplina(self):
        ofertaDisciplina_turma = self.turma
        ofertaDisciplina_professor = self.professor
        ofertaDisciplina_disciplina = self.disciplina
        ofertaDisciplina_diaDaSemana = "SEGUNDA"
        ofertaDisciplina_sala = self.sala
        ofertaDisciplina_horarioInicio = datetime.datetime.now().time()
        ofertaDisciplina_horarioFim = datetime.datetime.now().time()
        ofertaDisciplina = OfertaDisciplina.objects.create(
            turma=ofertaDisciplina_turma,
            professor=ofertaDisciplina_professor,
            disciplina=ofertaDisciplina_disciplina,
            diaDaSemana=ofertaDisciplina_diaDaSemana,
            sala=ofertaDisciplina_sala,
            horarioInicio=ofertaDisciplina_horarioInicio,
            horarioFim=ofertaDisciplina_horarioFim,
        )

        assert ofertaDisciplina.turma == ofertaDisciplina_turma
        assert ofertaDisciplina.professor == ofertaDisciplina_professor
        assert ofertaDisciplina.disciplina == ofertaDisciplina_disciplina
        assert ofertaDisciplina.diaDaSemana == ofertaDisciplina_diaDaSemana
        assert ofertaDisciplina.sala == ofertaDisciplina_sala
        assert ofertaDisciplina.horarioInicio == ofertaDisciplina_horarioInicio
        assert ofertaDisciplina.horarioFim == ofertaDisciplina_horarioFim

    def test_ofertaDisciplina_string_representation(self):
        assert (
            str(self.ofertaDisciplina)
            == f"{self.ofertaDisciplina.disciplina.nome} ({self.ofertaDisciplina.professor.nome}) {self.ofertaDisciplina.diaDaSemana} {self.ofertaDisciplina.horarioInicio} - {self.ofertaDisciplina.horarioFim}"
        )
