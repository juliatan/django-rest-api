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

- `vagrant up`, `vagrant ssh`, `cd /vagrant`, `source ~/env/bin/activate`.
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

### Viewsets

- Like APIViews, allow us to write logic for endpoints. Instead of writing functions that map to common HTTP methods, it accept functions that map to common API object actions e.g. list (ob jects), create, retrieve, update and destroy [an object].
- Perfect for standard database operations. Fastest way to make a database interface.
- Cases of when to use ViewSets over APIView:
  - A simple CRUD API on existing database model
  - A quick and simple API for pre-defined objects
  - Little to no customisation on the logic
  - Working with standard data structures
- Create a ViewSet by:
  - In `views.py`, create a class based on ViewSet.
  - Define the action methods.
  - Define the URL endpoint in `urls.py` and register our ViewSet through a router (provided by REST framework). Once then, add this to the urlpatterns (one time requirement).
- Check it works by going to the root of our API http://localhost:8000/api . You should be able to see the new URL we defined in the router. Note, this feature doesn't show APIView URLs.
- When defining the create method, we can use the same serializer concept as in the APIViews.

### Creating the profiles API

**Serializer**

- In the `serializers.py` file, create a `UserProfileSerializer` which inherits a `ModelSerializer`. Define the `Meta` class which is used to specify:
  - What the relevant model is
  - The fields to include
  - Extra settings e.g. to make the password write only and to style the field in the browsable API.
- In this case, we want to overwrite the `create` method to ensure the password input is saved as a hash. We also need to add an `update` method to handle the password hashing properly.

**Vietset**

- Next, create a viewset through a `viewsets.ModelViewset`. Designed to manage models through the API. Provide a queryset so it knows which objects will be managed.
- Django REST framework knows the standard functions we need like create, list, destroy and update. We just need to assign the `serializer_class` and `queryset` on which to perform these functions.

**URLs**

- In `urls.py`, register a new URL. We don't need to add a `base_name` because we defined a queryset in the viewset. This therefore allows it to default to the model in question. We can add a `base_name` if we want to override this.

**Test it works**

- Run `vagrant up`, `vagrant ssh`, `cd /vagrant`, `source ~/env/bin/activate`.
- Run `python manage.py runserver 0.0.0.0:8000` and go to http://localhost:8000/api/profile/
- We can now create a new user in the HTML form. Going to http://localhost:8000/api/profile/1/ also allows us to see and update the details for an individual user.

**Setup permissions**

- Create a new file called `permissions.py` to create a custom permission class. This will inherit from `BasePermission` which provides the `has_permission` and `has_object_permission` methods.
- SafeMethods are ones that don't make any changes to the object like GET. We want users to view other users' profiles, but only be able to change their profile. We do this by checking if the object ID they are trying to change matches the user_id making the request.
- Next, open `views.py` file and import TokenAuthentication. This utilised a random string that's appended to each request from the user.
- Add `authentication_classes = (TokenAuthentication,)` to the `UserProfileViewSet` class. Add a comma, to ensure it's added as a tuple. Note you can add more than one authentication class if you wish.
- Authentication classes sets method of authentication. Permission class sets the permission level. Add `permission_classes = (permissions.UpdateOwnProfile,)` which is the custom permissions class we just created.
- Test in the browser by going to http://localhost:8000/api/profile . We will be able to see all users' profile since GET is a safe method. If we go to http://localhost:8000/api/profile/1/ we will no longer be able to see the forms to update the user.

**Add filters**

- In the `views.py` file, add `filter_backends = (filters.SearchFilter,)` to the `UserProfileViewSet`.
- Also define the searchable fields
- Test in the browser by clicking on the new "filters" button. In effect, this adds a search param to the GET url. e.g. http://localhost:8000/api/profile/?search=test

**Add login API**

- In the `views.py` file, add `from rest_framework.authtoken.views import ObtainAuthToken` to import the `ObtainAuthToken` class.
- Add a new class called `UserLoginApiView` which inherits from `ObtainAuthToken`. Whilst we can add this directly to our URLs, it won't allow us to see this in our browsable API, so we need to override this and create our custom class.
- Do this by adding `renderer_classes`. Note that the ModelViewset comes with this as default.
- Go to `urls.py` and define a 'login/' url with our new `UserLoginApiView`.
- Test in the browser by going to http://localhost:8000/api/login/ . You should be able to see the token in the response when your submit your username and password. Make a note of the token.
- Use the ModHeader Chrome extension to add the token to the request header. (Authorization: Token <token>).
