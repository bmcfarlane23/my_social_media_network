# Brent McFarlane 05/20/2024  (added comments for my own understanding)
# imports the datetime module from the standard library and the SQLAlchemy class from the flask_sqlalchemy module.
import datetime
from flask_sqlalchemy import SQLAlchemy

# SQLAlechemy is an ORM (Object-Relational Mapping) library or database adapter object that allows us to interact with the database using Python objects.
# creates a new instance of the SQLAlchemy class and assigns it to the variable db.
db = SQLAlchemy()

# I want to create 4 tables: profiles, posts, images, and comments
# The Profile class inherits from the db.Model class, which is a base class for all models in Flask-SQLAlchemy.
class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    interests = db.Column(db.String(128))
    birthday = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    # The __init__ method is a constructor that initializes the Profile object with the username and password attributes.
    def __init__(self, username: str, password: str, name: str, start_date: datetime, interests=None, birthday=None):
        self.username = username
        self.password = password
        self.name = name
        self.interests = interests
        self.birthday = birthday
        self.start_date = start_date
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'interests': self.interests,
            'birthday': self.birthday.isoformat(),
            'start_date': self.start_date.isoformat(),
            'password' : 'Not shown for security reasons.'
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(128), nullable=False)
    post_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    likes = db.Column(db.Integer, default=0)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)

    def __init__(self, content:str, post_date: datetime, profile_id: int, likes:int = 0):
        self.content = content
        self.post_date = post_date
        self.likes = likes
        self.profile_id = profile_id
    
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'post_date': self.post_date.isoformat(),
            'likes': self.likes,
            'profile_id': self.profile_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(128), nullable=False)
    image_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id',))

    def __init__(self, url:str, image_date: datetime, post_id:int, comment_id:int = None):
        self.url = url
        self.image_date = image_date
        self.post_id = post_id
        self.comment_id = comment_id
    
    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'image_date': self.image_date.isoformat(),
            'post_id': self.post_id,
            'comment_id': self.comment_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(128), nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, content:str, comment_date: datetime, post_id:int):
        self.content = content
        self.comment_date = comment_date
        self.post_id = post_id
    
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'comment_date': self.comment_date.isoformat(),
            'post_id': self.post_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

# I now want to create 4 relationships: profile_posts, post_images, post_comments, and comment_images
# profile_posts will be a one-to-many relationship between profiles and posts
# post_images will be a one-to-many relationship between posts and images
# post_comments will be a one-to-many relationship between posts and comments
# comment_images will be a one-to-many relationship between comments and images


# If any of the relationships were many-to-many, I would have to create a join table to manage the relationship. 
# In this case I won't need to create a join table because the relationships are one-to-many but I added them below for personal reference and learning.

# class ProfilePost(db.Model):
#     __tablename__ = 'profile_posts'
#     profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

# class PostImage(db.Model):
#     __tablename__ = 'post_images'
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
#     image_id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

# class PostComment(db.Model):
#     __tablename__ = 'post_comments'
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
#     comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

# class CommentImage(db.Model):
#     __tablename__ = 'comment_images'
#     comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
#     image_id = db.Column(db.Integer, db.ForeignKey('images.id'), primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
