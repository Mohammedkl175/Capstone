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

    Assistant_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDMwMjQ3YjQyOGMwMDZhNzU5YjYyIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODUxNjEzLCJleHAiOjE2MTM4NTg4MTMsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyJdfQ.x0KDlY9s2kMXFpOI1dx8hmVH4uIJK_H9_SjjAldwSHuq34AJNyAovo7VUXddVFsAk15KQwOuIBtlLSfraP-PjxSP6TL2y6ZrZPGINhBApjKgBsp-INoAyn3DcOzyX7Z5tVdLHgAc1VO5zgr8DIDa8s_sa-VdY7j8PCt6hFpy7tq9BJA34dew42vAAGKsr1iU0eEAnhQ0yiQUjv0gBpByn5Yifyjuc_DvrNyWLPJ_qg8-KGhmHoiZ-thsAXF44ThhOoJ0nFk09Ie5wpTQuG0QrlpJuceQqZLqqYHq3xEfpG_-OiloNApVRGoj3ZHiDv-XwBDoIsq6Uu2bEaVy5hlJZg'
    Director_Token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzMDJlYzA0YTdjNjMwMDY4OGNiYjJjIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODUxNTQ0LCJleHAiOjE2MTM4NTg3NDQsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIl19.TUGhBcWzFgHYruxjoTfjfEQX0Mrd1XUg1_lgbwxeecNmedFLGna8RtnJ9YoL2a3nLjlpo1KgWRzYeP5L6mIFfWzGJWHDfQLbK6ENV8H5Y4IzK56qtO5_-GQWH_85UIiA3dzDoK19B_IBwtkhVCxijoAPNuGsJ5Rk2i4YNzk2o0TUNu-MabQ1s9K7jdQzO1DNLMGyPj4HdpaYyD7PVTc1l0jqO_vLgj6dWhMwIEeNFKabKtZM_5TOrJhmqa4XFQxcr1XbFk1FGbrERdIlYH1swZPogUnd5CTvnPkOpR8FLTYo4DwGRYLGD_3VEITb4fBSg8i_BLyiFE2sNJDtTw_Y3Q'
    Producer_Token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJnbnJKMEdFUGhXaTh2U01wN1hLUiJ9.eyJpc3MiOiJodHRwczovL2Rldi0tLXZkMjlndy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAyNmE5YjQyMTQxMGQwMDcxMjc0ZGUxIiwiYXVkIjoiY2Fwc3RvbmVwcm9qZWN0IiwiaWF0IjoxNjEzODUxNDMwLCJleHAiOjE2MTM4NTg2MzAsImF6cCI6Im5iTXM2WUtEelhhUXN5a0c5TTRqTUtoMWpvbFlMbmNPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3JzIiwiZ2V0OmFjdG9ycy1pbmZvIiwiZ2V0Om1vdmllcyIsImdldDptb3ZpZXMtaW5mbyIsInBhdGNoOmFjdG9yIiwicGF0Y2g6bW92aWUiLCJwb3N0OmFjdG9yIiwicG9zdDptb3ZpZSJdfQ.1SLjLuPy3gM54O1e-j3O9bmYpZRUJ1TbYP5sAN1OwYJN7q3d1SQtKRxE7rIlokdZVwAXNO3Jj9rs7ZE9x09X-ubKWHdKBvej2viG8WSnDUv8Yv8xMzv9gJ9AMXuA3XIxeLj-mJ3IyZY021sp7_6kk2dmlUjtlqi6HZDV-YnAzBMjNJgbzd6iN6HmHKcJSr2Ru_5yoBn-h0zMaE00DNLdQnjqnYqEkndPFSAwCRWMg2T2QRFROZoEBVdCVI_D5F9SKe1QKN6ZgTJvNf8Ml2EbMTychf3El4kXe0XEJz93scwDCU6mOZpHCPmk3YS3rrw6VdJ-xmjsM7A0SqFYdf4vIA'

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
