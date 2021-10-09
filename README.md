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
