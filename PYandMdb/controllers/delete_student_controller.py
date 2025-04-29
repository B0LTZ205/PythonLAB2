from flask import Blueprint, request, redirect, url_for, flash
from models.students_model import delete_student

# Create a blueprint for the 'delete' functionality

delete_bp = Blueprint('delete_student', __name__)

@delete_bp.route("/delete/<id>", methods=["POST"])

def delete_student_route(id):
    delete_student(id) # Perform db deletion
    flash("Student deleted successfully!","success" )
    return redirect(url_for("read_student.index")) # Redirect to main page after deletion
