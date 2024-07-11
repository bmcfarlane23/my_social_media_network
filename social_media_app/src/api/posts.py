# Brent McFarlane 05/25/2024  (added comments for my own understanding)
from flask import Blueprint, jsonify, abort, request
from ..models import Post, db 
from datetime import datetime

# This will output the URL prefix for the blueprint as /posts. If the URL for the database is http://localhost:3000 then the URL for this endpoint 
# would be http://localhost:3000/posts

bp_posts = Blueprint('posts', __name__, url_prefix='/posts')

# CRUD endpoint for Profile

# C: CREATE A RECORD
# The POST method is used to send data to the server to create a new user. 
@bp_posts.route('', methods=['POST'])
def create():
    if 'content' not in request.json or 'post_date' not in request.json or 'profile_id' not in request.json:
        return abort(400, description="Content, post date, and profile ID cannot be empty.")

    # construct Post
    p = Post(
        content=request.json['content'],
        post_date=request.json['post_date'],
        likes=request.json.get('likes', 0),
        profile_id=request.json['profile_id']
    )
    # The insert() method creates and adds the user to the database.
    p.insert()

    return jsonify(p.serialize())

# R: READ A RECORD
# Read all posts
@bp_posts.route('', methods=['GET']) 
def index():
    posts = Post.query.all()  # ORM performs SELECT query ( comparable to SELECT * FROM posts; )
    result = []
    for p in posts:
        result.append(p.serialize())  # build list of posts as dictionaries
    return jsonify(result)  # return JSON response

# Read a specific post
@bp_posts.route('/<int:id>', methods=['GET'])
def show(id: int):
    p = Post.query.get_or_404(id)
    return jsonify(p.serialize())  # return JSON response

# U: UPDATE A RECORD
# The PUT and PATCH methods are used to update a post in the database. 
@bp_posts.route('/<int:id>', methods=['PATCH','PUT'])
def update(id:int):
    # Retrieve the profile from the database with the specified id. If the profile does not exist, a 404 error is raised.
    p = Post.query.get_or_404(id)

    if 'content' not in request.json or 'post_date' not in request.json or 'likes' not in request.json or 'profile_id' not in request.json:
        return abort(400)
    
    # Content validation and update
    if 'content' in request.json:
        content = request.json['content']
        p.content = content

    # Content validation and update
    if 'post_date' in request.json:
        post_date = request.json['post_date']
        p.post_date = post_date

    # Likes validation and update
    if 'likes' in request.json:
        likes = request.json['likes']
        p.likes = likes

    try:
        p.update()  # commit the updates
        return jsonify(p.serialize())  # indicate success
    except:
        # something went wrong :(
        return jsonify(p.serialize())  # indicate failure

# D: DELETE A RECORD

@bp_posts.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    p = Post.query.get_or_404(id)
    try:
        p.delete()  # Delete and commit the deletion
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


# # I WANTED TO GET TO RELATIONSHIPS BUT COULDNT RUN CODE TO TEST
# # @bp_posts.route('/<int:id>/liked_tweets', methods=['GET'])
# # def liked_tweets(id: int):
# #     u = User.query.get_or_404(id)
# #     result = []
# #     # iterate through the liked_tweets relationship and serialize each user
# #     for t in u.liked_tweets:
# #         result.append(t.serialize())
# #     return jsonify(result)

