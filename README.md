<img src="docs/images/bookman.png" alt="logo" title="feishin" align="left" height="40" />

# Bookman

<img src="docs/images/Screenshot_20240121_181953.png"/>
Bookman is a django web-app developed as a project for Python in The Enterprise course.

It allows for library management by a librarian. It also allows for reverse image recognition for the use case of recognizing a book in the library using ORB and a Neural Network.

# Setting up dev env

To build the app yourself you need to take the following steps:

1. Clone the repo with `git clone https://github.com/robin-douziech/bookman.git` command

2. Create a virtual environment (recommended) and install dependencies

```shell
python -m venv .venv
source .venv/bin/activate.fish (or any other activation script)
pip install -r requirements/base.txt
```

3. Create the database file in _bookman_project_ folder with the name `db.sqlite3`
4. In folder _bookman_project/bookman_ create a new `.env` file with the following content:

```
TOKEN=django-insecure-sma61)9v5*hj(-6me1sl9=yt+ksto%c0+y(&s#i%_cftdjsn_^
ENVIRONMENT=DEV
```

5. Run manage.py and make the migrations, and then migrate

```shell
python bookman_project/manage.py makemigrations
python bookman_project/manage.py migrate
```

You can also create a superuser with the command

```shell
python bookman_project/manage.py createsuperuser
```

6. Finally run the server with `python bookman_project/manage.py runserver` and you should see the main page
