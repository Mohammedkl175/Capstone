import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actor, Movie,db_drop_and_create_all
from app import create_app


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "capstonetest"
        self.database_path = "postgresql://{}@{}:{}/{}".format("postgres","localhost","5432",self.database_name)
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app,self.database_path)
        db_drop_and_create_all()

        self.VALID_NEW_ACTOR = {
            "name": "Hisham Khalil",
            "age": 30,
            "gender":"Male"
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


    Assistant_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDMwMjQ3YjQyOGMwMDZhNzU5YjYyIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODYxMjEwLCJleHAiOjE2MTM4Njg0MTAsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyJdfQ.FWUbWsNgl5RbccwMNiXhSAS0dLG3lQh_wPldxZw2WU45T0cV5_ytdB4Crr-9_dhtaJm8YDWl7kz8BCxAYQU1ufgrWkhZZSSLcLC5_9hA9hhuMqOSptbfjLqYRJfcVwrEOuDq5TWiTMhue9AQzummjpWg0CsCXloJ3LkT-4gc9c1gEriALfoY5DUwMJxF5Uan4YiMP6YtuwXEf2sd-J5yd8CZ7kpfPVJQ8aBBly3GhDznktivsOwp587Nm9bdc3ZP5x5U433hm2EZ2vbllt5VF9Pi7TysDwkIb1UMA4aa6Y3st3ih2fo56oD40hoG7C2U_DA4A7z_Ib8X0TAPnCUN3A'
    Director_Token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDJlYzA0YTdjNjMwMDY4OGNiYjJjIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODYxMTU5LCJleHAiOjE2MTM4NjgzNTksImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.GMEkPSYqWiqqSngLtMytJti7Rk_yKggc7caV0VQCi39gRDzV9dDw-VBpSGyI6z_0nqdznNVCcHnoJiLIPCSUKRZPFOwFo1UBB6vG5FX4sb0bMBuRG0aikAsJ6EPLaRE8Xzvssw0OgYl-SbbpPl0nGMr8p5dq4oLWdWGT9PQVF9mw9XXJDuITnIYfUBd4UEGA1BOBctCqYT6xUX9wT_h3zrgJ12D1uT7GfiuBTDQJqwePh64-y_mRGOJ9Li1TTTB7VYHHz2BZCn38ub84jdUTF3pphTvQBdhlmn0A2txRUWsIStsBT88UkG5TNYAd-_qbbvoGiPZ0q7-bsNvZynwlSw'
    Producer_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyNmE5YjQyMTQxMGQwMDcxMjc0ZGUxIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODU5MDc1LCJleHAiOjE2MTM4NjYyNzUsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.PMAkzYVBaymZv3RAmD0xJIuZzYKW4eyqNNyO_3-3EEQg_yxrpUs4SLpydktziUbkiMQB7wWmpfOLzRFaQjZtrxEPIWLvu03mEEz8ShEYAXv20fyTdUlbJ5JgcoUnkTMwU67nSijs1DJhyYh4hVfEg61K1dAvHDnHmtToJD4w1RNZXgEnFybBHi3wynRnv_9b2fRsr0RjqzvxTc5DynFUKE6W7m-v1Dfoaun44kkitq_yXErQSoDcnNoUX486AXgKEnzqPgX5LoenBAJETnhi7Y1T1ePCn_Hes6SPY2qjdvdgiFSNG_kzhomAo3TIDsSjv5rCMVKtYY8lSM34GydEDg'

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
