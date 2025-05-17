from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users_model import add_user, get_user_by_email, get_user_by_username, verify_password
import re
from functools import wraps

# Create a blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Validation functions
def validate_registration(data):
    errors = []
    
    # Username validation
    if not data.get("username") or len(data.get("username", "")) < 3:
        errors.append("Username must be at least 3 characters.")
    
    # Email validation
    if not data.get("email") or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data["email"]):
        errors.append("Invalid email address.")
    
    # Password validation
    if not data.get("password") or len(data.get("password", "")) < 6:
        errors.append("Password must be at least 6 characters.")
    
    # Password confirmation
    if data.get("password") != data.get("confirm_password"):
        errors.append("Passwords do not match.")
    
    return errors

# Decorator for requiring login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for requiring admin role
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        if session.get('role') not in ['admin', 'superadmin']:
            flash("You don't have permission to access this page.", "danger")
            return redirect(url_for('read_student.index'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for requiring superadmin role
def superadmin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login'))
        if session.get('role') != 'superadmin':
            flash("You don't have permission to access this page.", "danger")
            return redirect(url_for('read_student.index'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Extract form data
        data = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "confirm_password": request.form.get("confirm_password"),
            "role": "user"  # Default role
        }
        
        # Validate input
        errors = validate_registration(data)
        
        # Check if username or email already exists
        if get_user_by_username(data["username"]):
            errors.append("Username already exists.")
        if get_user_by_email(data["email"]):
            errors.append("Email already exists.")
        
        if errors:
            return render_template("register.html", errors=errors, user=data)
        
        # Remove confirm_password before saving
        del data["confirm_password"]
        
        # Add user to database
        add_user(data)
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Find user by username
        user = get_user_by_username(username)
        
        # Check if user exists and password is correct
        if user and verify_password(user["password"], password):
            # Store user info in session
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            session["role"] = user["role"]
            
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("read_student.index"))
        else:
            flash("Invalid username or password.", "danger")
    
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    # Clear session
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile")
@login_required
def profile():
    # This route will show the user's profile
    return render_template("profile.html")