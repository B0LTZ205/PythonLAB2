from flask import flash
from flask import Blueprint, request, redirect, url_for, render_template
from models.students_model import get_all_students, update_student
import re

# Create a blueprint for the 'update' functionality

update_bp = Blueprint('update_student', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_input(data):
    errors = []
    if not data.get("studentid") or not re.match(r'^\d+', data["studentid"]):
        errors.append("Student ID must be digits.")
    if not data.get("name") or not re.match(r'^[A-Za-z ]+$', data["name"]):
        errors.append("Name must only contain letters and spaces.")
    if not data.get("email") or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data["email"]):
        errors.append("Invalid email address.")
    if not data.get("program") or not re.match(r'^[A-Za-z ]+$', data["program"]):
        errors.append("Program must only contain letters and spaces.")
    if not data.get("enrollmentdate") or not re.match(r'^\d{4}-\d{2}-\d{2}$', data["enrollmentdate"]):
        errors.append("Invalid enrollment date format (YYYY-MM-DD).") 
    return errors

# Route to handle POST request from the Add modal form
@update_bp.route("/update/<id>", methods=["POST"])
def update_student_route(id):
    # Extract form data from the request
    update_data = {
        "studentid": request.form.get("studentid"),
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "program": request.form.get("program"),
        "enrollmentdate": request.form.get("enrollmentdate")
    }

    # Validate input
    errors = validate_input(update_data)

    # Handle Image
    image_file = request.files.get("image")
    if image_file and image_file.filename!= "":
        if not allowed_file(image_file.filename):
            errors.append("Image file must be a PNG, JPG, JPEG, or GIF.")
    else:
        image_file = None

    # If errors, re-render page with error messages
    if errors:
        students = get_all_students()
        update_data["_id"] = id
        return render_template("index.html", students=students, errors=errors, student=update_data, edit_id = id)
    
    # Add student to database
    update_student(id, update_data, image_file)
    flash("Student updated successfully!","success" )
    # Redirect to main page after success
    return redirect(url_for("read_student.index"))
