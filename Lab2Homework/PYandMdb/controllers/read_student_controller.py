from flask import Blueprint, render_template
from models.students_model import get_all_students

# Create a blueprint for the 'read' functionality

read_bp = Blueprint('read_student', __name__)

# Route to display student list on homepage
@read_bp.route("/")
def index():
    students = get_all_students()
    return render_template("index.html", students=students)