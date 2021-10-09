# DJANGO REST API

## How it works

- Uses Vagrant to create a containerised application, which is run inside a Virtual Machine (I use Virtual Box on my MacBook Pro). Ensure you have installed this and enabled your MacBook to use Oracle's Virtual Box in the Securities & Preferences settings.
- To start Vagrant: `vagrant up`.
- Ensure you have a virtual environment setup in Vagrant. To do this, run `vagrant ssh`, `cd /vagrant`, and `python -m venv ~/env`.
- Activate the virtual environment: `source ~/env/bin/activate`.
- Install the requirements: `pip install -r requirements.txt`.

### One time setup of Django project

- `django-admin startproject profiles_project .`
- In `settings.py`, add 'rest_framework' and 'rest_framework.authtoken' to the INSTALLED_APPS list.

### Creating new apps

- Create the first app within the `profiles_project`: `python manage.py startapp profiles_api`.
- In `settings.py`, add 'profiles_api' to the INSTALLED_APPS list.

### Start Django web development server

- `python manage.py runserver 0.0.0.0:8000`
- Navigate browser to http://localhost:8000/

## Models

- Models are used by us to describe the data needed for our project.
- Django sets up the database using these models.
- Each model maps to a specific table in the database.
- Django manages the relationship between our models and database, so we don't need to interact with database directly.
- Docs: [https://docs.djangoproject.com/en/3.2/topics/db/models/](https://docs.djangoproject.com/en/3.2/topics/db/models/)

- NOTE: The User model is provided to us out of the box by Django. We can override this in the `models.py` file within the `profiles_api` app.

### Migration files

- Django creates migration files to ensure our database matches our models.
- In our vagrant directory and virtual environment, run `python manage.py makemigrations profiles_api`. This generates the migration file in the `migrations` folder of the app in question.
- Run `python manage.py migrate` to apply the migration file to the database. This goes through our entire project and runs all migration files.
