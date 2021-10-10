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

- `python manage.py runserver 0.0.0.0:8000`. If there's an infinite loop situation, try `python manage.py runserver 0.0.0.0:8000 --noreload`
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

## Using the Django admin dashboard

- In `admin.py`, import the model(s) from the various apps.
- Dashboard is accessible at http://localhost:8000/admin/
- Auth Token comes from the Django REST framework. Authentication and authorization comes from Django out of the box.
- User profiles is automatically deduced from the way we called our UserProfile. It also pluralises it.

## Django REST Framework

- Offers some helper methods to help us create our API endpoints.
- The Django REST framework Views provided are the APIView and ViewSet classes.

### APIView

- Most basic type of view to build our API. Is similar to a traditional Django View but specifically for APIs.
- Describes the logic that makes up an API endpoint. Gives us the most control over our application logic.
- Allows us to match standard HTTP methods: GET, POST, PUT, DELETE.
- Might be better to use this when:
  - Need full control over the logic (e.g. multiple data sources).
  - Processing files and rendering a synchronous response.
  - Call other APIs / services in the same response.
  - Accessing local files or data.
- Create an APIView by:
  - Open `profiles_api/views.py`. Create class based on APIView class.
  - Define HTTP methods to handle. Each method must return a `Response` object. The `Response` object takes in either a list or dictionary (to allow it to convert to JSON).
  - Define a URL endpoint and assign it to this new view.
- To define a URL endpoint:
  - In our `profiles_api` app, create a `urls.py` file.
  - In `urls.py`, be sure to import `include` from `django.urls`. This allows us to include other app URLs into our root.
  - Add a URL to the list.

### Serializer

- Provided by Django REST framework. Allows us to easily converts data inputs into Python objects and vice versa.
- In our `profiles_api` app, create a `serializers.py` file.
- Our serializers should specify the fields we want to accept from the client. Similar to Django forms. They also take care of validation rules that are required for the fields.
- Hook this up to our APIView in `profiles_api/views.py`.
- Check it works by going to http://localhost:8000/api/hello-view/ and testing it out through the browsable API.
