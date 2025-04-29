from flask import flash
from flask import Blueprint, render_template, request, redirect, url_for
from models.students_model import add_student, get_all_students
import re

# Create a blueprint for the 'create' functionality

create_bp = Blueprint('create_student', __name__)

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
@create_bp.route("/add", methods=["POST"])
def add_student_route():
    # Extract form data from the request
    data = {
        "studentid": request.form.get("studentid"),
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "program": request.form.get("program"),
        "enrollmentdate": request.form.get("enrollmentdate")
    }

    # Validate input
    errors = validate_input(data)

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
        return render_template("index.html", students=students, errors=errors, student=data)
    
    # Add student to database
    add_student(data, image_file)
    flash("Student added successfully!","success" )
    # Redirect to main page after success
    return redirect(url_for("read_student.index"))
