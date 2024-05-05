import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db_drop_and_create_all
bearer_tokens = {
    "casting_assistant" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkltTnltbU84N01acTdiQ0JyNTN3byJ9.eyJpc3MiOiJodHRwczovL2Rldi1jcGFhNmU0eWVsbXA2MnVhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjM0ZjdlOGMyNTNhMTcyYWZmNDRiMmUiLCJhdWQiOiJDYXN0aW5nIiwiaWF0IjoxNzE0ODMxODE4LCJleHAiOjE3MTQ5MTgyMTgsInNjb3BlIjoiIiwiYXpwIjoibnZlejBUaTV6SnVoWnhJV3FTNHROc1p4bnNkMkg0aE8iLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.Tjxe-XrZIg_VBcDNahasBJlbs1Y14xxGS_3vVzXn2vcEn3G8YdZXaErFMhtPv-SEHlk3T5OoECfqafQ2FeCSNTUghCruWueTdDWbPzgwFrC65PPjvuZt7q-MSPh6HynkS7RrjtRHpB_wRb6qORebaN6h1Z8tTS5sNg2JLoNemIOqynUdGkUQF3omxAwNEQKHRHS-bWPrDOVQVCgX8nP-sWHOAWyeXOpMKlWxIw8bLdhADg1m4oBYv1VaWbmTq26nfy6GWyJba4oI4Hr_c6kvo_9p27mq2029bDxbwDpeOIIoobyvbDIxouWDRs2Ebyb38j0qL7UJv2o0TLWx7ed5Mw",
    "casting_director" : "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkltTnltbU84N01acTdiQ0JyNTN3byJ9.eyJpc3MiOiJodHRwczovL2Rldi1jcGFhNmU0eWVsbXA2MnVhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjM1ZjZmMDE3Zjk5YTc0ZDNhMzhkYWEiLCJhdWQiOiJDYXN0aW5nIiwiaWF0IjoxNzE0ODMxOTAzLCJleHAiOjE3MTQ5MTgzMDMsInNjb3BlIjoiIiwiYXpwIjoibnZlejBUaTV6SnVoWnhJV3FTNHROc1p4bnNkMkg0aE8iLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3JzIiwiYWRkOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.ze-5hLFR6DKLdR5OjjVod1TxkfRuyOvpiSG8ZNfkdm6qcG7LHWXQGCcXLHTOTd-s6F47BkXqKb0yUi9Jm9WNTnZ85Y4VYiQTnOr0AOGU7cRJs-QCApm3Bl7ipUVuon5MAKODYysVHIW5I3a1AztDwnirEMziB_zbPx61tgeI_sQWq1wMoCzhbAa8BRLwlo9-2900p_c2fgD17xKDBmC8orOxPVD1ABCXG7T2YcEVtWTTxSozuXYCXCx2mRjqMYxH_Q84xrnyfJ7_YRQffyZuO1-DTeKe-oFCRJjHbxssz2pQ0wOkM1xbvZN-hLs99zmEHDs8Q5jutwt3we4iGU971g"
    }
casting_assistant_auth_header = {
        'Authorization': bearer_tokens['casting_assistant']
    }

casting_director_auth_header = {
        'Authorization': bearer_tokens['casting_director']
    }
class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        setup_db(self.app)
        db_drop_and_create_all()
        self.app.testing = True
        self.client = self.app.test_client

    def tearDown(self):
        pass


    def test_add_movie(self):
        create_movie = {
            'title': 'ABC XYZ',
            'release_year': 2024
        }
        res = self.client().post('/movies/create', json=create_movie, headers = casting_director_auth_header)
        data = json.loads(res.data)
        print("test_add_movie \n")
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_get_movies(self):
        res = self.client().get('/movies', headers = casting_assistant_auth_header)

        data = json.loads(res.data)
        print("test_get_movies \n")
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_add_actor(self):
        create_actor = {
            'name': 'Trung',
            'age': 30,
            'gender': 'male',
            'movie_id': 1
        } 

        res = self.client().post('/actors/create', json = create_actor, headers = casting_director_auth_header)
        data = json.loads(res.data)
        print("test_add_actor \n")
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_actors(self):
        res = self.client().get('/actors', headers = casting_assistant_auth_header)

        data = json.loads(res.data)
        print("test_get_actors \n")
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie(self):
        res = self.client().patch(
            '/movies/update/1',
            json={
                'title': 'Updated title of movie'}, headers = casting_director_auth_header)
        data = json.loads(res.data)
        print("test_update_movie \n")
        print(data)
        self.assertEqual(res.status_code, 200)

    def test_update_actor(self):
        res = self.client().patch(
            '/actors/update/1',
            json={
                'age': 10000}, headers = casting_director_auth_header)
        data = json.loads(res.data)
        print("test_update_actor \n")
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor(self):
        delete_actor = {
            'name': 'Delete',
            'age': 19,
            'gender': 'male',
            'movie_id': 1
        } 

        res = self.client().post('/actors/create', json = delete_actor, headers = casting_director_auth_header)
        data = json.loads(res.data)
        res = self.client().delete('/actors/delete/' + str(data['actor_id']), headers = casting_director_auth_header)
        data = json.loads(res.data)
        print("test_delete_actor \n")
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        Delete_movie = {
            'title': 'Delete_movie',
            'release_year': 2024
        }
        res = self.client().post('/movies/create', json=Delete_movie, headers = casting_director_auth_header)
        data = json.loads(res.data)
        res = self.client().delete('/movies/delete/' + str(data['movie_id']), headers = casting_director_auth_header)
        data = json.loads(res.data)
        print("test_delete_movie \n")
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == '__main__':
    unittest.main()
