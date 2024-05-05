# Full Stack Casting API Backend

## About
This is my final capstone project for Udacity's FullStack Web Developer Nanodegree.

## Getting Started

### Installing Dependencies

#### Python 3.10

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Run the following to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Running the server

To run the server, execute:
* run ```pip install -r requirements.txt``` 
* export ```DATABASE_URL``` to environment variables of your system. Use ```export DATABASE_URL={username}:{password}@{host}:{port}/{database_name}```
* run ```export FLASK_APP=app.py```
* run ```flask run```

##API Endpoints

#### GET /movies
Returns a list of all available movies in the database.

Sample response output:
{'movies': [{'id': 1, 'release_year': 2024, 'title': 'First Movie'}], 'success': True}

#### GET /actors
Returns a list of all actors/actresses in the database

Sample response output:
{'actors': [{'age': 25, 'gender': 'male', 'id': 1, 'movie_id': 1, 'name': 'First'}], 'success': True}

#### POST /movies/create
Creates a new movie in the database.

Sample response output:
{'movie_id': 2, 'success': True}

#### POST /actors/create
Creates a new actor/actress in the database.

Sample response output:
{'actor_id': 2, 'success': True}

#### PATCH /movies/update/<movie_id>
Updates movie information

Sample response output:
{'movie_id': 1, 'success': True}

#### PATCH /actors/update/<actor_id>
Updates actor/actress information

Sample response output:
{'actor_id': 1, 'success': True}

#### DELETE /movies/delete/<movie_id>
Deletes a movie from the database

Sample response output:
{'deleted': 2, 'success': True}

#### DELETE /movies/actors/<actor_id>
Deletes a actor/actress from the database

Sample response output:
{'deleted': 2, 'success': True}

## Testing
There are 8 unittests in tests.py. To run this file use:
```
python tests.py
```
Output:
```
postgres@LPP00097115L:~/capstone$ python3 tests.py
test_add_actor

{'actor_id': 2, 'success': True}
.test_add_movie

{'movie_id': 2, 'success': True}
.test_delete_actor

{'deleted': 2, 'success': True}
.test_delete_movie

{'deleted': 2, 'success': True}
.test_get_actors

{'actors': [{'age': 25, 'gender': 'male', 'id': 1, 'movie_id': 1, 'name': 'First'}], 'success': True}
.test_get_movies

{'movies': [{'id': 1, 'release_year': 2024, 'title': 'First Movie'}], 'success': True}
.test_update_actor

{'actor_id': 1, 'success': True}
.test_update_movie

{'movie_id': 1, 'success': True}
.
----------------------------------------------------------------------
Ran 8 tests in 4.314s

OK
```
## THIRD-PARTY AUTHENTICATION
#### auth.py
Auth0 is set up and running:
- The Auth0 Domain Name
- The JWT code signing secret
- The Auth0 Client ID
The JWT token contains the permissions for the 'casting_assistant' and 'casting_director' roles.

