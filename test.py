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

    Assistant_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDMwMjQ3YjQyOGMwMDZhNzU5YjYyIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODMyMDQ5LCJleHAiOjE2MTM4MzkyNDksImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyJdfQ.1SYP22o__VHVJXK8UpGv0CizXMF313gm2ABr384a8oLv08bXhg5w7gVsgp-x_jNmYVYE5fjRHrNcStnfE-MQOZ6M-LGdsZZ8jQd6nrgEJvVNUcE5HmknJhlixhYy_kU-ZTFOp7XaT0gapUEmeqPmIlGsnFhMNCgaH1n0ode_0NdNl9M192W1xZRMx9cNw8YEpx3ca7vwM1jS5dTU8AeV-w_9RWEqjK5nWEHFS-EQ0gKptrVM-u3OqCUFB9c0sFtvmDG6FYfq0G5eY4qtVW9O-Ledfi5B745C996iInlW8T9ePyHlcoi0Nq2EgMAqlZSL0TgHRRgy-8wRTeVTHmcUng'
    Director_Token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDJlYzA0YTdjNjMwMDY4OGNiYjJjIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODI3MTg5LCJleHAiOjE2MTM4MzQzODksImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.zyMqVk7Apd5tgmUBIkDtdnNvGXlIj_rX7ehyuuKwqZS_W3wkkL8-vbR7kzKto-eW9HqKJrCoHjaJuwWZOlW0jtKUWJOa2BaZJqyrn8vn7Mf84Vsnu01sqgmO39KpKzNSrX6wV6cWcin9rE8L1nza3wNNQDGgDj49zOCBeJxuY-NtO1-r4g3MCbrbo5J3CEEBBzZMkXXgTCBUrpnWSKAgI8m-sj7xcZBhuDqNCcgGPTLBISklBXWQNQaufyro5bncxPQHOaJrhgf_Bp6XAhH-vYhi6JBqypYvTpWMC4N2OrT54OGf7aoicwLldphQH0qErVnJue0KScA96cmQohB2Yg'
    Producer_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyNmE5YjQyMTQxMGQwMDcxMjc0ZGUxIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODMxOTc1LCJleHAiOjE2MTM4MzkxNzUsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.NvkfRJ2kfiRl_paA9oHJ5GxeahrM7IBOwLyo8puumsYHaYxI4o6o1S6YdUwQWOCESLUDBJhg-tFxoBXO-xJDjsiDCEidM73xTjsXFVrwG9mr1Ybi8rXYhIniqbaxuoZh4OCZfiHQT7cJrusb9CGTvaFKMK8LI5QpkBlDrTs5TXyHaxjO46LZ-nrePJqkHiSzXuhpyii_J_NvxuYcdVfmL-JEheMc_90KQ6slsBLdBnKTb9O3sqLkcmZSCgXZH3dSqV5SuKmSmBVaOxxd8daAFphT1Ch-wxgcO-MXrVvwhz_AbLukKIvkz_liRdLTKT4V0k--CEqPkLfdSSCjdI3-3g'

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
