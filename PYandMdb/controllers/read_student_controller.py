from flask import Blueprint, render_template, Response
from models.students_model import get_all_students, db
from bson import ObjectId
import gridfs

fs = gridfs.GridFS(db)  # Connect to your MongoDB database named 'db' and a collection named 'fs' for storing images.  # Replace 'db' and 'fs' with your actual database and collection names.  # Note: If you're using a different database or collection, replace 'db' and 'fs' with your actual database and collection names.  # Also, ensure you've installed the 'pymongo' and 'flask-pymongo
# Create a blueprint for the 'read' functionality

read_bp = Blueprint('read_student', __name__)

# Route to display student list on homepage
@read_bp.route("/")
def index():
    students = get_all_students()
    return render_template("index.html", students=students)

@read_bp.route("/image/<image_id>")
def save_image(image_id):
    try:
        image_file = fs.get(ObjectId(image_id))
        return Response(image_file.read(), mimetype=image_file.content_type)
    except Exception as e:
        return "Image not found", 404