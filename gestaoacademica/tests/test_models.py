from django.test import TestCase
from django.db.utils import IntegrityError

from model_bakery.baker import make

from authenticator.models import User
from gestaoacademica.models import Aluno


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
