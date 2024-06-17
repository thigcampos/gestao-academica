# Sistema de Gestão Acadêmica

## Shortcuts
- [Access RN01 tests](https://github.com/thigcampos/gestao-academica/blob/837a970028bac04d98bb00752e189d34e2f321b7/gestaoacademica/tests/test_views.py#L105)
- [Access RN02 test](https://github.com/thigcampos/gestao-academica/blob/837a970028bac04d98bb00752e189d34e2f321b7/gestaoacademica/tests/test_views.py#L223)
- [Access coverage report](https://github.com/thigcampos/gestao-academica/blob/main/report.txt)
For more relevant information, access our document file, [available here](https://docs.google.com/document/d/1wjidif7AT5nD9yiiaksyZcpWJWkPXzqrcJdchuTGczU/edit?usp=sharing).

## Setup local environment
### 0. Clone this repo
Before cloning, make sure you add your public SSH key in github.
```
$ git clone git@github.com:thigcampos/gestao-academica.git
```
And cd into the root folder:
```
cd gestao-academica
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

#### 1.3 Run migrations:
```
python manage.py makemigrations
```

Then, run:

```
python manage.py migrate
```

#### 1.4 Populate the database
Give `execute` permissions to our setup script:
```
chmod +x setup.sh
```

Then, run it:
```
./setup.sh
```
### 2. Run server
```
pipenv run ./manage.py runserver 8000
```
It should be up and running in http://localhost:8000.
You can also access http://localhost:8000/admin.

### 3. Run tests
```
pipenv run pytest
```

### 4. Run cov erage
```
pipenv run coverage run -m pytest
```

Open coverage details:
```
pipenv run coverage html
```

### 5. Generate UML 
```
./manage.py generate_puml
```
