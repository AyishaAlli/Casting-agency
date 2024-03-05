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

# Create a PostgreSQL database engine
engine = create_engine(database_path, echo=True)

# Base class for declarative models
Base = declarative_base()

movie_actor_association = Table('movie_actor_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date)
    description = Column(String)

    # Define the many-to-many relationship with Actor
    actors = relationship("Actor", secondary=movie_actor_association, back_populates="movies")

    def __init__(self, title, release_date, description):
        self.title = title
        self.release_date = release_date
        self.description = description

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
            'description':self.description,
            'release_date': self.release_date
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(Base):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    image = Column(String)

    # Define the many-to-many relationship with Movie
    movies = relationship("Movie", secondary=movie_actor_association, back_populates="actors")

    def __init__(self, name, image, age, gender):
        self.name = name
        self.image = image
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
            'image':self.image,
            'age': self.age,
            'gender': self.gender
        }

    def __repr__(self):
        return json.dumps(self.format())

# Create the tables in the database
Base.metadata.create_all(engine)