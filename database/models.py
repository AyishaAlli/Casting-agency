from flask_migrate import Migrate
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, create_engine
from sqlalchemy.orm import declarative_base, relationship
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']


db = SQLAlchemy()

'''
setup_db(app)
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()


'''
    drop and create the database tables
    can be used to initialize a clean database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # Add some initial data
    actors = [
            Actor(name='Lisa Ann', age=18, gender='Female'),
            Actor(name='Rita Bekket', age=22, gender='Female'),
            Actor(name='Michelle Jones', age=25, gender='Female'),
            Actor(name='Matt Harris', age=37, gender='Male'),
        ]

    for actor in actors:
        actor.insert()

    movies = [
            Movie(title='Mighty Men', release_date='2024-07-16'),
            Movie(title='No way out', release_date='2025-09-23'),
            Movie(title='the ultimagte Parody', release_date='2024-10-14')
        ]

    for movie in movies:
        movie.insert()





class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)


    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    '''
        insert a new model into a database
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
        delete a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
        update a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
        inserts a new model into a database
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
        updates a new model into a database
        the model must exist in the database

    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return json.dumps(self.format())
    

