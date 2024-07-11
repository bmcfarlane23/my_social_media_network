# Brent McFarlane 05/25/2024  (added comments for my own understanding)

# Import the Blueprint, jsonify, abort, and request classes from the flask module.
from flask import Blueprint, jsonify, abort, request
# Import the Profile, Post, Image, Comment, and db classes from the models module.
from ..models import Profile, db 
import hashlib
import secrets
from datetime import datetime

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

# Create a new Blueprint object called bp with the name 'users' and the URL prefix '/users'.
# if the URL for the database is http://localhost:3000 then the URL for this endpoint would be http://localhost:3000/users
# bp = Blueprint('users', __name__, url_prefix='/users')
bp_profiles = Blueprint('profiles', __name__, url_prefix='/profiles')

# CRUD endpoint for Profile

# C: CREATE A RECORD
# The POST method is used to send data to the server to create a new user. 
@bp_profiles.route('', methods=['POST'])
def create():
    # Check if the request contains the required fields
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    start_date_str = request.json['start_date']
    
    # Optional field interests
    interests = request.json.get('interests', None)
    
    # Optional field birthday
    birthday_str = request.json.get('birthday', None)

    # Additional check for non-empty strings
    if not username or not password or not name or not start_date_str:
        return abort(400, description="Username, password, name, and/or start date cannot be empty.")

    # Check if the start_date is in the correct format
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    except ValueError:
        return abort(400, description="Start date must be in YYYY-MM-DD format.")

    birthday = None
    if birthday_str:
        try:
            birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
        except ValueError:
            return abort(400, description="Birthday must be in YYYY-MM-DD format if provided.")

    # construct Profile
    p = Profile(
        username=username,
        password=scramble(password),
        name=name,
        interests=interests,
        birthday=birthday,
        start_date=start_date
    )
    # The insert() method creates and adds the user to the database.
    p.insert()

    return jsonify(p.serialize())

# R: READ A RECORD
# Read all record
@bp_profiles.route('', methods=['GET']) 
def index():
    profiles = Profile.query.all()  # ORM performs SELECT query ( comparable to SELECT * FROM profiles; )
    result = []
    for p in profiles:
        result.append(p.serialize())  # build list of profiles as dictionaries
    return jsonify(result)  # return JSON response

# Read a specific record
@bp_profiles.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Profile.query.get_or_404(id)
    return jsonify(p.serialize())  # return JSON response

# U: UPDATE A RECORD
# The PUT and PATCH methods are used to update a user in the database. The code needs to be able to handle a username only, a password only, and both
# username and password being updated.
@bp_profiles.route('/<int:id>', methods=['PATCH','PUT'])
def update(id:int):
    # Retrieve the profile from the database with the specified id. If the profile does not exist, a 404 error is raised.
    p = Profile.query.get_or_404(id)

    if 'username' not in request.json or 'password' not in request.json or 'name' not in request.json or 'start_date' not in request.json:
        return abort(400)
    
    # Username validation and update
    if 'username' in request.json:
        username = request.json['username']
        # return 400 if username is less than 3 characters
        if len(username) < 3:
            return abort(400)
        # update username
        p.username = username

    # Password validation and update
    if 'password' in request.json:
        password = request.json['password']
        if len(password) < 8:
            return abort(400)
        p.password = scramble(password)

    # Name validation and update
    if 'name' in request.json:
        name = request.json['name']
        p.name = name
    
    # Start date validation and update
    if 'start_date' in request.json:
        start_date_str = request.json['start_date']
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            p.start_date = start_date
        except ValueError:
            return abort(400, description="Start date must be in YYYY-MM-DD format.")
    
    # Interests validation and update
    if 'interests' in request.json:
        interests = request.json['interests']
        p.interests = interests
    
    # Birthday validation and update
    if 'birthday' in request.json:
        birthday_str = request.json['birthday']
        if birthday_str:
            try:
                birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
                p.birthday = birthday
            except ValueError:
                return abort(400, description="Birthday must be in YYYY-MM-DD format if provided.")
        else:
            p.birthday = None

    try:
        p.update()  # commit the updates
        return jsonify(p.serialize())  # indicate success
    except:
        # something went wrong :(
        return jsonify(p.serialize())  # indicate failure

# D: DELETE A RECORD

@bp_profiles.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Profile.query.get_or_404(id)
    try:
        p.delete()  # Delete and commit the deletion
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


# # I WANTED TO GET TO RELATIONSHIPS BUT COULDNT RUN CODE TO TEST
# # @bp_profiles.route('/<int:id>/liked_tweets', methods=['GET'])
# # def liked_tweets(id: int):
# #     u = User.query.get_or_404(id)
# #     result = []
# #     # iterate through the liked_tweets relationship and serialize each user
# #     for t in u.liked_tweets:
# #         result.append(t.serialize())
# #     return jsonify(result)

