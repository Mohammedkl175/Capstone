import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actor, Movie, db_drop_and_create_all
from app import create_app


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "capstonetest"
        self.database_path = "postgresql://{}@{}:{}/{}".format(
            "postgres", "localhost", "5432", self.database_name)
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        self.VALID_NEW_ACTOR = {
            "name": "Hisham Khalil",
            "age": 30,
            "gender": "Male"
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

    Assistant_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDMwMjQ3YjQyOGMwMDZhNzU5YjYyIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzOTA3NTY2LCJleHAiOjE2MTM5MTQ3NjYsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyJdfQ.rik24YqM2jXby3wRmjKnBorQMNztgALYbfxCKOeQk6v9pKecpc1LdrHnhH4lHnYc4wQnT7RjPqgp4MXFdeQ5UFAP3kCzYG75zX3byYdDFw5D5YCYucoDpmM-U2YDUrak0KkyoGjG0Xpjy2WFbMQv4NJEhvyvEJipvRCI0rLtG_WJP5nvUdtbhIHwywcaJQGDVabxgzvnKkTDcXlDhgxJB-J4-xc6FGdIrXL6CVuSc0DGz8EU_xe1mGHfE8lIrV3PIAkizAygCejQ0hOW8CQXYg7FY9tS-bBhjMR1kmm3ne8xnHT9hB-_zoeAhmk8LZFHoyiRvDTEIwRHtnqiWdBBYw'
    Director_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDJlYzA0YTdjNjMwMDY4OGNiYjJjIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzOTA3NTAwLCJleHAiOjE2MTM5MTQ3MDAsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.FXaox4-486oPUOLxTsBLnjsCEWhbHqNoCbX_3sPf9B1MxSh0Z_Zo35Y9gM8gSf5_vL-sNS5BEP14a9JH8nHtej9jlm_UmdT5NOieEj5wQ-mASzjZH0Ykl1lEGAZgIOINeWh_gPzcGCv3GxMOfkeTQc6GEhwmGrutYDV53SJSvuwYzCklXDErCQItuqP8Dj3KzJ-TS3KfBG4FaAx6KVonJQthJbbYo5IS3H7O3nFz8ntf2tTqxjCmzKx4w1YKT3wgMXN4h5Gg3yCOUhNhEVxyhi7xn-sP7CiWmTT2gJY15MDNwYhOagXvCXcjdaI2OFmuxFexmSoCMZAhy0f1OeESFQ'
    Producer_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyNmE5YjQyMTQxMGQwMDcxMjc0ZGUxIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzOTA3Mzc0LCJleHAiOjE2MTM5MTQ1NzQsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.aNbul253v_mPTJSo8-zO8Rw3Hqq5U9N8Ndc95ouBQjI0Nicn5k79sBEvk-4m3tFZA3hR1rUYnWdmGMsgnpIUWMfwE9Uawt5XEMBAWr9ABcSPjBTg2U4DlPndCCli2C99m9D9JoeV06xqEBLPLQ6JyvUPrLl_VfoEaHqvNhv93IecLF2KTfNNJDkkJnXCXusWgGJ1ONbGC9JXzoSmScLWBzJx3bdqbkQrkwOkADjnJfzp2oVWB-uHojghHFWihleGj1Olv7zQhCLNsQYxPJNcYYMPLTl-zPrK-kuc3VXEk3WVVIGDyubquyvoeXz4O4Ups11QHL0eWfjzkDwxEyDVBw'

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
            'Authorization': "Bearer {}".format(self.Producer_Token)
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
