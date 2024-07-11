# Brent McFarlane 05/25/2024  (added comments for my own understanding)
from flask import Blueprint, jsonify, abort, request
from ..models import Image, db 


bp_images = Blueprint('images', __name__, url_prefix='/images')

# CRUD endpoint for images

# C: CREATE A RECORD
# The POST method is used to send data to the server to create a new images. 
@bp_images.route('', methods=['POST'])
def create():
    if 'url' not in request.json or 'image_date' not in request.json or "post_id" not in request.json or "comment_id" not in request.json:
        return abort(400)

    # construct Image
    i = Image(
        url=request.json['url'],
        image_date=request.json['image_date'],
        post_id=request.json['post_id'],
        comment_id=request.json['comment_id']
    )
    # The insert() method creates and adds the user to the database.
    i.insert()

    return jsonify(i.serialize())

# # R: READ A RECORD
# # Read all images
@bp_images.route('', methods=['GET']) 
def index():
    images = Image.query.all()  # ORM performs SELECT query ( comparable to SELECT * FROM profiimagesles; )
    result = []
    for i in images:
        result.append(i.serialize())  # build list of images as dictionaries
    return jsonify(result)  # return JSON response

# Read a specific image
@bp_images.route('/<int:id>', methods=['GET'])
def show(id: int):
    i = Image.query.get_or_404(id)
    return jsonify(i.serialize())  # return JSON response

# # U: UPDATE A RECORD
# # The PUT and PATCH methods are used to update a images in the database. The code needs to be able to handle a username only, a password only, and both
# # username and password being updated.
@bp_images.route('/<int:id>', methods=['PATCH','PUT'])
def update(id:int):
    # Retrieve the profile from the database with the specified id. If the profile does not exist, a 404 error is raised.
    i = Image.query.get_or_404(id)

    if 'url' not in request.json or 'image_date' not in request.json:
        return abort(400)

    # URL validation and update
    if 'url' in request.json:
        url = request.json['url']
        i.url = url

    # Image date validation and update
    if 'image_date' in request.json:
        image_date = request.json['image_date']
        i.image_date = image_date

    try:
        i.update()  # commit the updates
        return jsonify(i.serialize())  # indicate success
    except:
        # something went wrong :(
        return jsonify(i.serialize())  # indicate failure

# # D: DELETE A RECORD

@bp_images.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    i = Image.query.get_or_404(id)
    try:
        i.delete()  # Delete and commit the deletion
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)



# # I WANTED TO GET TO RELATIONSHIPS BUT COULDNT RUN CODE TO TEST
# # @bp_images.route('/<int:id>/liked_tweets', methods=['GET'])
# # def liked_tweets(id: int):
# #     u = User.query.get_or_404(id)
# #     result = []
# #     # iterate through the liked_tweets relationship and serialize each user
# #     for t in u.liked_tweets:
# #         result.append(t.serialize())
# #     return jsonify(result)

