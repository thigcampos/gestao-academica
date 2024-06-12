echo "Criando usuários:"
cat setup/base_users.py | python3 manage.py shell
echo "Usuários criados"
echo "Criando Alunos:"
cat setup/base_alunos.py | python3 manage.py shell
echo "Alunos criados"
echo "Criando Professores:"
cat setup/base_professores.py | python3 manage.py shell
echo "Professores criados"
echo "Criando Disciplinas:"
cat setup/base_disciplina.py | python3 manage.py shell
echo "Disciplinas criadas"


