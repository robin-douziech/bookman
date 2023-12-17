# Bookman
---
Bookman is a django web-app developed as a project for Python in The Enterprise course.

It allows for library management by a librarian.

More to come as we develop the app

# Setting up dev env
To build the app yourself you need to take the following steps:

1. Clone the repo with `git clone https://github.com/robin-douziech/bookman.git` command
2. Checkout to a branch of your liking. Right now the most up to date and somewhat stable branch is `dev` though if you want to test out new features any of the `feature-*` branch is an option.

```bash
git checkout dev
```

3. Create a virtual environment (recommended) and install dependencies

```shell
python -m venv .venv
source .venv/bin/activate.fish (or any other activation script)
pip install -r requirements/base.txt
```

4. Create the database file in *bookman_project* folder with the name `db.sqlite3`
5. In folder *bookman_project/bookman* create a new `.env` file with the following content:

```
TOKEN=django-insecure-sma61)9v5*hj(-6me1sl9=yt+ksto%c0+y(&s#i%_cftdjsn_^
ENVIRONMENT=DEV
```

6. Run manage.py and make the migrations, and then migrate

```shell
python bookman_project/manage.py makemigrations
python bookman_project/manage.py migrate
```

7. Finally run the server with `python bookman_project/manage.py runserver` and you should see the main page