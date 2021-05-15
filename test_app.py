
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
from dotenv import load_dotenv


auth_manager_header = {

'Authorization': os.environ.get('MANAGER_TOKEN')
}
auth_barista_header = {

 'Authorization': os.environ.get('BARISTA_TOKEN')
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

#Delete drink by Manager
    def test_delete_drink_by_manager(self):
        res = self.client().delete('/drinks/28', headers=auth_manager_header)
        data = json.loads(res.data)

        drink = Drink.query.filter(Drink.id == 28).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

#Test Barista has no access to delete drinks
    def test_delete_drink_by_barista(self):
        res = self.client().delete('/drinks/28',headers=auth_barista_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], {'code': 'unauthorized', 'description':'Permission not found.'})



#test_404_delete_drink_not_exist
    def test_404_delete_drink_not_exist(self):
        res = self.client().delete('/drinks/1000',headers=auth_manager_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

#test_401_delete_drink_unauth
    def test_401_delete_drink_unauth(self):
        res = self.client().delete('/drinks/2',header=auth_manager_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['code'], 'unauthorized')
   

#Add new drink by Manager

    def test_post_drink_by_manager(self):
        res = self.client().post('/drinks', headers=auth_manager_header,
            json={
                "title": "Strawberry",
                "recipe": [{"color": "green", "name": "Strawberry", "parts": 2}],
                "category_id": 1
                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

#Test Barista has no access to adding drinks
    def test_create_new_drink_by_barista(self):
        res = self.client().post('/drinks',headers=auth_barista_header,
        json={
                "title": "Strawberry small",
                "recipe": [{"color": "green", "name": "Strawberry", "parts": 2}],
                "category_id": 1
                })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'], {'code': 'unauthorized', 'description':'Permission not found.'})



#Test failing add drink
    def test_400_fail_create_drink(self):
        res = self.client().post('/drinks',json={},headers=auth_manager_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], 'bad request structure') 



#Test unauthorized creating drink
    def test_401_unauth_create_drink(self):
        res = self.client().post('/drinks',headers=auth_manager_header,
        json={
                "title": "Apple",
                "recipe": [{"color": "green", "name": "apple", "parts": 2}],
                "category_id": 1
                }
        
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')   

#Update current drink_by_manager
    def test_update_drink_by_manager(self):
        res = self.client().patch('/drinks/28',headers=auth_manager_header,
          json={
                "title": "Water",
                "recipe": [{"color": "white", "name": "water", "parts": 2}],
                "category_id": 2
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
#Update current drink_by_Barista
    def test_update_drink_by_barista(self):
        res = self.client().patch('/drinks/28',headers=auth_barista_header,
          json={
                "title": "Water",
                "recipe": [{"color": "white", "name": "water", "parts": 2}],
                "category_id": 2
                }
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], True)


#Test update drink not exist

    def test_404_update_drink_not_exist(self):
        res = self.client().patch('/drinks/999',headers=auth_manager_header,
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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
