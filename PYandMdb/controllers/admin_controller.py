from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.users_model import get_all_users, get_user_by_id, update_user, delete_user, add_user
from controllers.auth_controller import admin_required, superadmin_required
import re

# Create a blueprint for admin functionality
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Validation function for user data
def validate_user_data(data, is_update=False):
    errors = []
    
    # Username validation
    if not data.get("username") or len(data.get("username", "")) < 3:
        errors.append("Username must be at least 3 characters.")
    
    # Email validation
    if not data.get("email") or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data["email"]):
        errors.append("Invalid email address.")
    
    # Password validation (only check if it's provided or if it's a new user)
    if not is_update or (is_update and data.get("password")):
        if not data.get("password") or len(data.get("password", "")) < 6:
            errors.append("Password must be at least 6 characters.")
    
    return errors

# Routes
@admin_bp.route("/")
@admin_required
def admin_dashboard():
    users = get_all_users()
    return render_template("admin/dashboard.html", users=users)

@admin_bp.route("/users")
@admin_required
def list_users():
    users = get_all_users()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/users/add", methods=["GET", "POST"])
@superadmin_required  # Only superadmins can add users
def add_user_route():
    if request.method == "POST":
        # Extract form data
        data = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "role": request.form.get("role", "user")
        }
        
        # Superadmin check - only superadmins can create admin/superadmin users
        if data["role"] in ["admin", "superadmin"] and session.get("role") != "superadmin":
            flash("You don't have permission to create admin or superadmin users.", "danger")
            return redirect(url_for("admin.list_users"))
        
        # Validate input
        errors = validate_user_data(data)
        
        if errors:
            return render_template("admin/add_user.html", errors=errors, user=data)
        
        # Add user to database
        add_user(data)
        flash("User added successfully!", "success")
        return redirect(url_for("admin.list_users"))
    
    return render_template("admin/add_user.html")

@admin_bp.route("/users/edit/<user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = get_user_by_id(user_id)
    
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin.list_users"))
    
    # Check permissions - only superadmins can edit other superadmins or admins
    if session.get("role") != "superadmin" and (user.get("role") == "superadmin" or user.get("role") == "admin"):
        flash("You don't have permission to edit this user.", "danger")
        return redirect(url_for("admin.list_users"))
    
    if request.method == "POST":
        # Extract form data
        data = {
            "username": request.form.get("username"),
            "email": request.form.get("email"),
            "role": request.form.get("role")
        }
        
        # Only include password if it was provided
        password = request.form.get("password")
        if password:
            data["password"] = password
        
        # Role permission check - only superadmins can assign admin or superadmin roles
        if data["role"] in ["admin", "superadmin"] and session.get("role") != "superadmin":
            flash("You don't have permission to assign admin or superadmin roles.", "danger")
            return redirect(url_for("admin.list_users"))
        
        # Validate input
        errors = validate_user_data(data, is_update=True)
        
        if errors:
            return render_template("admin/edit_user.html", errors=errors, user=data, user_id=user_id)
        
        # Update user in database
        update_user(user_id, data)
        flash("User updated successfully!", "success")
        return redirect(url_for("admin.list_users"))
    
    # Remove password from user object for security
    if "password" in user:
        del user["password"]
    
    return render_template("admin/edit_user.html", user=user, user_id=user_id)

@admin_bp.route("/users/delete/<user_id>", methods=["POST"])
@superadmin_required  # Only superadmins can delete users
def delete_user_route(user_id):
    user = get_user_by_id(user_id)
    
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("admin.list_users"))
    
    # Check permissions - admins can't delete superadmins, and can only delete other admins if they are superadmin
    if (user.get("role") == "superadmin" or 
        (user.get("role") == "admin" and session.get("role") != "superadmin")):
        flash("You don't have permission to delete this user.", "danger")
        return redirect(url_for("admin.list_users"))
    
    # Prevent self-deletion
    if str(user["_id"]) == session.get("user_id"):
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("admin.list_users"))
    
    # Delete user from database
    delete_user(user_id)
    flash("User deleted successfully!", "success")
    return redirect(url_for("admin.list_users"))