echo "Criando usuários:"
cat setup/base_users.py | python3 manage.py shell

