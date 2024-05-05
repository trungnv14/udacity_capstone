import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
database_path = os.environ['DATABASE_URL']

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)



def create_tables():
    with db.app.app_context():
        db.create_all()
        print("Tables created successfully!")

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    first_actor = (Actor(
        name = 'First',
        gender = 'male',
        age = 25,
        movie_id = 1
        ))

    first_movie = (Movie(
        title = 'First Movie',
        release_year = 2024
        ))
    first_movie.insert()
    first_actor.insert()
    db.session.commit()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    release_year = Column(Integer())
    actors = db.relationship('Actor', backref='movies')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    age = Column(Integer())
    gender = Column(String())

    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movies.id'),
        nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
