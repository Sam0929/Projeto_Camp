<h1 align="center"> Projeto Camp </h1>

### Passo a passo acesso ao projeto

Clone Repositório criado a partir do template, entre na pasta e execute os comandos abaixo:

Crie um ambiente virtual e ative-o:
```sh
python -m venv venv
venv\Scripts\activate
```

Instale o Django:
```sh
pip install Django
```

Faça as migrations do bando de dados:
```sh
python manage.py makemigrations
```

Suba as migrations:
```sh
python manage.py migrate
```

Se quiser povoar o banco de dados, execute:
```sh
python manage.py adicionar_dados
```

Para iniciar o server:
```sh
python manage.py runserver
```

Acesse o site:
```sh
localhost:8000/home
```


