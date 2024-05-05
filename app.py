from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

from auth import AuthError, requires_auth
from models import setup_db, Movie, Actor, db_drop_and_create_all


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    setup_db(app)
    db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, True')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, PATCH, OPTIONS')
        return response

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'success': True,
            'description': 'Running.'
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('view:movies')
    def get_movies(jwt):
        movies = Movie.query.all()

        if not movies:
            abort(404, {'message': 'no movies found in DB.'})

        movies = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': movies
        })

    @app.route('/movies/create', methods=['POST'])
    @requires_auth('add:movies')
    def add_movie(jwt):

        body = request.get_json()
        if not body:
          abort(400, {'message': 'invalid JSON body.'})

        title = body.get('title')
        release_year = body.get('release_year')

        if not title:
            abort(422, {'message': 'no title provided.'})
        if not release_year:
            abort(422, {'message': 'no "release_year" provided.'})

        movie = Movie(title=title, release_year=release_year)
        movie.insert()

        return jsonify({
            'success': True,
            'movie_id': movie.id
        })

    @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie:
            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie_id
            })
        else:
            abort(404, {'message': 'Movie with id {} not found in DB.'.format(movie_id)})

    @app.route('/movies/update/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(jwt, movie_id):
        body = request.get_json()

        title = body.get('title')
        release_year = body.get('release_year')
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if title:
            movie.title = title
        if release_year:
            movie.release_year = release_year

        movie.update()

        return jsonify({
            'success': True,
            'movie_id': movie.id
        })


    @app.route('/actors', methods=['GET'])
    @requires_auth('view:actors')
    def get_actors(jwt):
        actors = Actor.query.all()

        if not actors:
            abort(404, {'message': 'can not find any actors in DB'})

        actors = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': actors
        })

    @app.route('/actors/create', methods=['POST'])
    @requires_auth('add:actors')
    def add_actor(jwt):
        body = request.get_json()
        if not body:
          abort(400, {'message': 'invalid JSON body.'})
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        movie_id = body.get('movie_id')

        if not (name and age and gender and movie_id):
            abort(422, {'message': 'no name or gender or movie_id provided.'})

        actor = Actor(name=name,
                      age=age,
                      gender=gender,
                      movie_id=movie_id)
        actor.insert()

        return jsonify({
            'success': True,
            'actor_id': actor.id
        })


    @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(jwt, actor_id):
        actor = Actor.query.get(actor_id)

        if actor:
            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor_id
            })
        else:
            abort(400, {'message': 'an actor id doesnt have in DB'})

    @app.route('/actors/update/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actors(jwt, actor_id):
        actor = Actor.query.get(actor_id)

        if actor:
                body = request.get_json()

                name = body.get('name')
                age = body.get('age')
                gender = body.get('gender')
                movie_id = body.get('movie_id')

                if name:
                    actor.name = name
                if age:
                    actor.age = age
                if gender:
                    actor.gender = gender
                if movie_id:
                    actor.movie_id = movie_id

                actor.update()

                return jsonify({
                    'success': True,
                    'actor_id': actor.id
                })

        else:
            abort(404, {'message': 'Actor with id {} not found in DB.'.format(actor_id)})

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(AuthError)
    def authentification_failed(AuthError): 
        return jsonify({
            "success": False, 
            "error": AuthError.status_code,
            "message": AuthError.error['description']
            }), AuthError.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
