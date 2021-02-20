import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actor, Movie
from app import create_app


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "capstonetest"
        self.database_path = "postgresql://{}@{}:{}/{}".format("postgres","localhost","5432",self.database_name)
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app,self.database_path)

        self.VALID_NEW_ACTOR = {
            "name": "Haneen Tayseer",
            "age": "27",
            "gender":"Female"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Mohammed Khalil"
        }

        self.VALID_UPDATE_ACTOR = {
            "name": "Haneen Arrabi"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "3 Brothers",
            "release_year": 2000,
        }

        self.INVALID_NEW_MOVIE = {
            "title": "3 Brothers",
        }

        self.VALID_UPDATE_MOVIE = {
            "release_year": 2018
        }

        self.INVALID_UPDATE_MOVIE = {}

        # binds the app to the current context
        #with self.app.app_context():
            #self.db = SQLAlchemy()
            #self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()

    Assistant_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDMwMjQ3YjQyOGMwMDZhNzU5YjYyIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODQ0NDA1LCJleHAiOjE2MTM4NTE2MDUsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyJdfQ.ikS9YpCwmdzY7k5Gkx198yyRKT0egJjS7cgdfqMacREfFl-p-ErkP-TSUc1u3C5XfrLz71NUG0pSrQww4vFq46SEQpb6X4QP33vU2aQYffvqyH6Tp_1s7g45Qq3CmRn_q27aIvs9cjD9G5uqXTmvGl-Iqk1HvUYcPgGZSGUmnzIxw8Veaqx8J4j0Ui-qjwb-sgKctS8o1xj01iu2Yd9vhBGcgT3LXn-E6thwNxrDmSBooykZN81PoF_h1kh7-VL_-a6lmtGB3ddLliXCy022QRJPQksx1vQczK9RnkFx6ZwR92djYVzsUe-29la1wMW-HxXqoKDyT6fFkj6vFLr2rQ'
    Director_Token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDJlYzA0YTdjNjMwMDY4OGNiYjJjIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODQ0NDc1LCJleHAiOjE2MTM4NTE2NzUsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.jq0Jnn3qpBY1Rv3WYmljh-tKQU319hCItqp6B8PStH3hQHbBDmS5wzem0RvR1YSmLZWUZf7i-Gjtx64pxSMVIEoqCNWRELbsiVqbJskGEbM-CY-xS2sQDwrsS79g7Vx5R7eVRBGCQEHYpLH76xCkxYv5eI8h5nEeJkr6zVH00or6N1ttommA3nNQuJWBTi5WLQHKMYWZTZsgvnvdxzDbSDbqYUMkpjOYHzbPmReqdvBHHNYWUTjlKpVKO_SeH6Jav_zoR9YrrWgLwgWWMR5hGkTm5404h-vE-NpmEgpn4cYXQ4nNmnzQbr3mbnG8GgFtpoDB8ZqLpDx45O3IZ7P4jA'
    Producer_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyNmE5YjQyMTQxMGQwMDcxMjc0ZGUxIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODQzNjk2LCJleHAiOjE2MTM4NTA4OTYsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.NreD6CajKe-7LzCgGacBpWavjOC5u-cZpbQvnN77SWZoaUwqtAmYtk4HT8fdOmW3EC1wFzEse6FhWxHn3iL2HdUIvaneTttQ6OGq7mLbSNvFzNYvwyTA1dHxgKm4CdKaPUWx5sS-kJPXWJ_NASVxlPY-nmEx7srL7ljIO6OcIPY_XRh177_icDaVN6fiQV8At7IQqdJQrATmWtWRc0eQktPFr37qwNRWI_zV227IpW8daRVsZDgtavAprJdJafhFXetQ22VjKcbMmOHaKyb-Vgn5sTROB1gq7KZRxqbTF5tG5rusu5UmSu2YIvxvT75TnVVihURcPYAxxmhQ5wjNcQ'

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        """Passing Test for GET /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.Assistant_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertTrue(len(data["actors"]))

    def test_get_actors_by_id(self):
        """Passing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/2', headers={
            'Authorization': "Bearer {}".format(self.Assistant_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor', data)

    def test_404_get_actors_by_id(self):
        """Failing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/200', headers={
            'Authorization': "Bearer {}".format(self.Assistant_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_actor(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.Director_Token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_422_create_actor(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.Director_Token)
        }, json=self.INVALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_update_actor_info(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/2', headers={
            'Authorization': "Bearer {}".format(self.Director_Token)
        }, json=self.VALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.Director_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.Director_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.Assistant_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id(self):
        """Passing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.Assistant_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_get_movie_by_id(self):
        """Failing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.Assistant_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_movie(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.Producer_Token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_422_create_movie(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.Producer_Token)
        }, json=self.INVALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])

    def test_update_movie_info(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/2', headers={
            'Authorization': "Bearer {}".format(self.Director_Token)
        }, json=self.VALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_422_update_movie_info(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.Director_Token)
        }, json=self.INVALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.Producer_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.Producer_Token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
