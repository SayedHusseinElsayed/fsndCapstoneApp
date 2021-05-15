
from jose import jwt
from jose.jws import _encode_payload
from auth import verify_decode_jwt
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine, DateTime
from app import create_app
from models import *
from auth import AuthError, requires_auth, verify_decode_jwt


auth_header = {

'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InlNbE5IR3BabHdqalJyTHBERzhrbSJ9.eyJpc3MiOiJodHRwczovL3Bvcy1jb2ZmZWUtc2hvcC51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDA1ODcwMDkwNzk0NjU3OTM3MjAiLCJhdWQiOiJjb2ZmZWVzaG9wIiwiaWF0IjoxNjIxMDM1MzcxLCJleHAiOjE2MjEwNDI1NzEsImF6cCI6IjQzOFlVNGpJODVpYk9aQnJjdmlSbGdhMzRxVFhWUDc2Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6IGNhdGVnb3JpZXMiLCJkZWxldGU6ZHJpbmtzIiwiZ2V0OmNhdGVnb3JpZXMiLCJnZXQ6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmNhdGVnb3JpZXMiLCJwb3N0OmRyaW5rcyJdfQ.j7wo6T5oSfnfuPITjQsGZgrSrt_s7Dqm-kkXmHTSj5t3sVGJBEMB2l3zgkhyT9WL-mJiTveDXPzjDcPfhZNUJmWHBhBjYzyXr-K-WuggjKd5faHscHsXI6BOmb6Jczw4uWxkYyvcYA4805F-hXOK6nRtjEOp6ywIs2c67tDC_DX5T-BARHJ8ynz9h14uAu3Xj4AkC4IHB5--PxJI3NenfIkBY0qwT2OoRkZkGweLOQl9lWQRV26TbaTowkUTPk4NKLpibMwYUDEy0ilGv1nu1epQadeAZ8emqZv_QdAm8qOL9yKIa6nhcslU5-L-ERkPgjyiNZ6ctS--QJx8dxeGcw"

}

class CoffeeShopTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
    
        self.database_name = "coffee_shop"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', self.database_name)
        setup_db(self.app)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass

#Get All drinks
    def test_get_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['drinks'])


#Get All categories
    def test_get_categries(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])


#Delete drink
    def test_delete_drink(self):
        res = self.client().delete('/drinks/2', headers=auth_header)
        data = json.loads(res.data)

        drink = Drink.query.filter(Drink.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
   
'''
#Add new drink
    def test_post_drink(self):
        res = self.client().post('/drinks', headers=auth_header,
            json={
                "title": "Strawberry",
                "recipe": [{"color": "green", "name": "Strawberry", "parts": 2}],
                "category_id": 1
                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


#Test failing add drink
    def test_400_fail_create_drink(self):
        res = self.client().post('/drinks',json={},headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request structure') 


#Test unauthorized 
    def test_401_unauth_create_drink(self):
        res = self.client().post('/drinks',headers=auth_header,
        json={
                "title": "Apple",
                "recipe": [{"color": "green", "name": "apple", "parts": 2}],
                "category_id": 1
                }
        
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')   

#Update current drink
    def test_update_drink(self):
        res = self.client().patch('/drinks/28',headers=auth_header,
          json={
                "title": "Water",
                "recipe": [{"color": "white", "name": "water", "parts": 2}],
                "category_id": 2
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

  

#Test delete drink not exist
    def test_404_delete_drink_not_exist(self):
        res = self.client().delete('/drinks/1000',headers=auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')



#Test update drink not exist

    def test_404_update_drink_not_exist(self):
        res = self.client().patch('/drinks/999',headers=auth_header,
          json={
                "title": "Water",
                "recipe": [{"color": "white", "name": "water", "parts": 2}],
                "category_id": 2
                }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

'''
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
