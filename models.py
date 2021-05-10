import os
import sys
from sqlalchemy import Column, String, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

import json


database_name = "d5pjp6023975ed"
database_path = "postgres://{}:{}@{}/{}".format('postgres', 'root', 'localhost:5432', database_name)


db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    drink = Drink(
        title='Nescafee',
        recipe='[{"name": "Nescafee", "color": "black", "parts": 2}]'
    )


class Drink(db.Model):
    # Autoincrementing, unique primary key
    id           = Column(Integer(), primary_key=True)
    # String Title
    title        = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe       = Column(String(180), nullable=False)
    #category_id  = db.Column(db.Integer, db.ForeignKey('Category.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
   

  
    def short(self):
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe,
            'category_id': self.category_id
        }


    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe),
            'category_id': self.category_id
        }



    def insert(self):
        db.session.add(self)
        db.session.commit()



    def delete(self):
        db.session.delete(self)
        db.session.commit()



    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Category(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String name
    name = Column(String(80), unique=True)
    children = relationship("Drink")
   

    def __init__(self, name):
        self.name = name

    def format(self):
        return {
        'id': self.id,
        'name': self.name
        }
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def long(self):
        return {
            'id': self.id,
            'name': self.name
        }
