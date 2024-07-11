# Brent McFarlane 05/25/2024 
from flask import Blueprint, jsonify, abort, request
from ..models import Profile, Post, Image, Comment, db 


bp_comments = Blueprint('comments', __name__, url_prefix='/comments')

# CRUD endpoint for Profile

# C: CREATE A RECORD
# The POST method is used to send data to the server to create a new user. 
@bp_comments.route('', methods=['POST'])
def create_comment():
    if 'content' not in request.json or 'comment_date' not in request.json or 'post_id' not in request.json:
        return abort(400, description="Content, comment date, and post ID cannot be empty.")

    # Construct Comment object
    c = Comment(
        content=request.json['content'],
        comment_date=request.json['comment_date'],
        post_id=request.json['post_id']
    )

    # The insert() method creates and adds the user to the database.
    c.insert()

    return jsonify(c.serialize())

# # R: READ A RECORD
# # Read all comments
@bp_comments.route('', methods=['GET']) 
def index():
    comments = Comment.query.all()  # ORM performs SELECT query ( comparable to SELECT * FROM coments; )
    result = []
    for c in comments:
        result.append(c.serialize())  # build list of profiles as dictionaries
    return jsonify(result)  # return JSON response

@bp_comments.route('/<int:id>', methods=['GET'])
# Read a specific comment
def show(id: int):
    c = Comment.query.get_or_404(id)
    return jsonify(c.serialize())  # return JSON response

# # U: UPDATE A RECORD
# # The PUT and PATCH methods are used to update a user in the database. The code needs to be able to handle a username only, a password only, and both
# # username and password being updated.
@bp_comments.route('/<int:id>', methods=['PATCH','PUT'])
def update(id:int):
    # Query the database for the comment with the specified id. If the comment does not exist, a 404 error is raised.
    c = Comment.query.get(id)

    if c is None:
        return abort(404, description="Comment not found.")

    # Validate the request JSON and required fields
    if not request.json or 'content' not in request.json or 'comment_date' not in request.json or 'post_id' not in request.json:
        return abort(400, description="Content, comment date, and post ID cannot be empty.")


    # Content validation and update
    if 'content' in request.json:
        content = request.json['content']
        c.content = content

    # Comment date validation and update
    if 'comment_date' in request.json:
        comment_date = request.json['comment_date']
        c.comment_date = comment_date

    # Post ID validation and update
    if 'post_id' in request.json:
        post_id = request.json['post_id']
        c.post_id = post_id

    
    try:
        c.update()  # commit the updates
        return jsonify(c.serialize())  # indicate success
    except:
        # something went wrong :(
        return jsonify(c.serialize())  # indicate failure

# # D: DELETE A RECORD

@bp_comments.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    c = Comment.query.get_or_404(id)
    try:
        c.delete()  # Delete and commit the deletion
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

