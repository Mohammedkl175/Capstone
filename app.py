from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth
import os


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    db_drop_and_create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response


    @app.route('/actors')
    @requires_auth("get:actors")
    def get_actors(payload):
        try:
            actors_query = Actor.query.all()
            actors = [actor.short() for actor in actors_query]

            return jsonify({
                "success": True,
                "actors": actors
            })
        except:
            abort(422)

    @app.route('/actors/<int:id>')
    @requires_auth("get:actors-info")
    def get_actor_by_id(id):
        actor = Actor.query.get(id)
        if actor is None:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "actor": actor.long()
                })

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actor")
    def create_actor(payload):
        try:
            request_body = request.get_json()
            if 'name' not in request_body or 'age' not in request_body or 'gender' not in request_body:
                raise KeyError

            if request_body['name'] == '' or request_body['age'] == '' or request_body['gender']=='':
                raise ValueError

            new_actor = Actor(request_body['name'],
                              request_body['age'],request_body['gender'])
            new_actor.insert()

            return jsonify({
                "success": True,
                "created_actor_id": new_actor.id
            })

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth("patch:actor")
    def update_actor(id):
        actor = Actor.query.get(id)
        try:
            if actor is None:
                abort(404)
            else:
                request_body = request.get_json()
                if not bool(request_body):
                    raise TypeError

                if "name" in request_body:
                    if request_body["name"] == "":
                        raise ValueError

                    actor.name = request_body["name"]

                if 'age' in request_body:
                    if request_body["age"] == "":
                        raise ValueError

                    actor.age = request_body["age"]

                if 'gender' in request_body:
                    if request_body["gender"] == "":
                        raise ValueError

                    actor.gender = request_body["gender"]

                actor.update()

                return jsonify({
                    "success": True,
                    "actor_info": actor.long()
                    })

        except (TypeError, ValueError, KeyError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth("delete:actor")
    def delete_actor(id):
        actor = Actor.query.get(id)

        if actor is None:
            abort(404)
        else:
            actor.delete()
            return jsonify({
                "success": True,
                "deleted_actor_id": actor.id
                })

    @app.route('/movies')
    @requires_auth("get:movies")
    def get_movies(payload):
        try:
            movies_query = Movie.query.all()
            movies = [movie.short() for movie in movies_query]

            return jsonify({
                "success": True,
                "movies": movies
                })
        except:
            abort(422)

    @app.route('/movies/<int:id>')
    @requires_auth("get:movies-info")
    def get_movie_by_id(id):
        movie = Movie.query.get(id)
        if movie is None:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "movie": movie.long()
                })

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movie")
    def create_movie(payload):
        try:
            request_body = request.get_json()

            if 'title' not in request_body or 'release_year' not in request_body:
                raise KeyError

            if request_body['title'] == '' or request_body['release_year'] < 1:
                raise TypeError

            new_movie = Movie(
                request_body['title'],
                request_body['release_year']
            )

            new_movie.insert()

            return jsonify({
                "success": True,
                "created_movie_id": new_movie.id
                })

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth("patch:movie")
    def update_movie(id):
        movie = Movie.query.get(id)

        try:
            if movie is None:
                abort(404)
            else:
                request_body = request.get_json()
                if not bool(request_body):
                    raise TypeError

                if "title" in request_body:
                    if request_body["title"] == "":
                        raise ValueError

                    movie.title = request_body["title"]

                if "release_year" in request_body:
                    if request_body["release_year"] <= 0:
                        raise ValueError

                    movie.release_year = request_body["release_year"]

                movie.update()

                return jsonify({
                    "success": True,
                    "movie_info": movie.long()
                    })

        except (TypeError, ValueError, KeyError):
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth("delete:movie")
    def delete_movie(id):
        movie = Movie.query.get(id)

        if movie is None:
            abort(404)
        else:
            movie.delete()
            return jsonify({
                "success": True,
                "deleted_movie_id": movie.id
                })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource Not Found"
            }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method Not Allowed"
            }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad Request"
            }), 400

    @app.errorhandler(401)
    def Unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': "Unauthorized"
            }), 401

    @app.errorhandler(403)
    def Forbidden(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': "Forbidden"
            }), 403

    @app.errorhandler(500)
    def Server_Error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal Server Error"
            }), 500

        
    return app

APP = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

