# Sistema de Gestão Acadêmica

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

### 4. Run coverage
```
pipenv run coverage run -m pytest
```

Open coverage details:
```
pipenv run coverage html
```

