# Sistema de Gestão Acadêmica

## Setup local environment
### 0. Clone this repo
Before cloning, make sure you add your public SSH key in github.
```
$ git clone git@github.com:thigcampos/alunos.git
```
And cd into the root folder:
```
cd alunos
```

### 1. Install packages
#### 1.0 Install pipenv
```
pip install pipenv
```
New to pipenv? No problem! Read more [here](https://realpython.com/pipenv-guide/).

#### 1.1 Copy env variables
```
cp env.example .env
```
Pipenv will look for this file (.env) in order to export environment variables into your shell.

#### 1.2 Start your virtualenv:
```
pipenv shell
```

#####  1.2 Install packages (using Pipfile.lock):
```
pipenv install --ignore-pipfile
```
Now, let's setup the database.

### 2. Database setup (postgres)
You can use `docker-compose` or use postgres locally in your machine. If you choose docker, simply run:

```shell
docker compose up
```
If you find any issues, you can check [common issues](#common-issues) section.
#### 2.0 Install asdf:
See instructions [here](https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies).

#### 2.1 Install db (postgres)
Before proceeding, make sure you have the correct [dependencies](https://github.com/smashedtoatoms/asdf-postgres#dependencies) installed.
```
asdf plugin-add postgres
asdf install postgres 14.2
asdf local postgres 14.2
```
Notice that `asdf` creates a `.tool-versions` file in the current directory.
Every time you switch to this directory `asdf` will take over and use that version of postgres.

#### 2.2 Setup db
First, let's start our db server with:
```
postgres
```
Second, in another shell session let's setup user, password and the database we are going to need:
```
sudo -u postgres ~/.asdf/installs/postgres/14.2/bin/psql 
OR 
psql -U postgres (inside your environment using pipenv)

postgres=# CREATE USER admin WITH PASSWORD 'admin';
postgres=# CREATE DATABASE gestaoacademica WITH OWNER admin;
postgres=# ALTER USER admin CREATEDB;
```
Third, change `DATABASE_URL` in `.env` with the correct user and password chosen above.

Now, let's django migrate:
```
pipenv run ./manage.py migrate
```
Finally, create your django superuser with:
```
pipenv run ./manage.py createsuperuser
```

### 3. Run server
```
pipenv run ./manage.py runserver 8000
```
It should be up and running in http://localhost:8000.
You can also access http://localhost:8000/admin.

### 4. Run tests
```
pipenv run pytest
```

### 5. Run coverage
```
pipenv run coverage run -m pytest
```

Open coverage details:
```
pipenv run coverage html
```

### Common issues

#### `role does not exist`
After setting up your postgres database and try to run the django application, you might get an authentication error. In docker logs, you might view something like:
```
FATAL:  role "postgres" does not exist
```
To address that issue, you will need to stop your postgreSQL container and remove it. Then, once you start a new container, your issue will be resolved.

#### `password authentication failed`
Initially, you might want to check if `POSTGRES_PASSWORD` and `DATABASE_URL` variables are both correct. If so, I would recommend you to delete `postgres-data` folder and try to re-launch the docker container.

#### `postgres-data/__init__py: Permission Denied` while runnning `pytest`
As suggested in [this GitHub issue](https://github.com/docker-library/postgres/issues/392#issuecomment-408110910), you may want to add a `.dockerignore` with postgres-data in it. If `.dockerignore` doesn't fix this particular issue, you may want to check this [stackoverflow post](https://github.com/docker-library/postgres/issues/392#issuecomment-408110910).
