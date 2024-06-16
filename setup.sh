pipenv run ./manage.py makemigrations
pipenv run ./manage.py migrate
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
echo "Criando Salas:"
cat setup/base_salas.py | python3 manage.py shell
echo "Salas criadas"
echo "Criando Ofertas de disciplinas:"
cat setup/base_oferta_disciplina.py | python3 manage.py shell
echo "Ofertas de disciplinas criadas"

pipenv run ./manage.py runserver 8000