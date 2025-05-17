from flask import Flask, session, redirect, url_for, flash, request
from controllers.create_student_controller import create_bp
from controllers.read_student_controller import read_bp
from controllers.update_student_controller import update_bp
from controllers.delete_student_controller import delete_bp
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
import functools

app = Flask(__name__)

# Register blueprints
app.register_blueprint(create_bp)
app.register_blueprint(read_bp)
app.register_blueprint(update_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

app.secret_key = "your-secret-key"

# Role-based access control middleware
@app.before_request
def check_user_permissions():
    # Public routes that don't require authentication
    public_routes = [
        'auth.login', 
        'auth.register', 
        'auth.logout',
        'read_student.index',
        'read_student.save_image',
        'static'
    ]
    
    # Check if the current route is public
    if request.endpoint in public_routes or request.endpoint is None:
        return  # Allow access to public routes
    
    # Check if user is logged in
    if 'user_id' not in session:
        flash("Please log in to access this feature.", "warning")
        return redirect(url_for('auth.login'))
    
    # Admin-only routes
    admin_routes = [
        'admin.admin_dashboard',
        'admin.list_users',
        'admin.add_user_route',
        'admin.edit_user',
        'admin.delete_user_route',
        'create_student.add_student_route',
        'update_student.update_student_route',
        'delete_student.delete_student_route'
    ]
    
    # Superadmin-only routes
    superadmin_routes = [
        # Routes that only superadmins can access
    ]
    
    # Check permissions for admin routes
    if request.endpoint in admin_routes and session.get('role') not in ['admin', 'superadmin']:
        flash("You don't have permission to access this feature.", "danger")
        return redirect(url_for('read_student.index'))
    
    # Check permissions for superadmin routes
    if request.endpoint in superadmin_routes and session.get('role') != 'superadmin':
        flash("You don't have permission to access this feature.", "danger")
        return redirect(url_for('read_student.index'))

# Make session available to all templates
@app.context_processor
def inject_user():
    return {
        'session': session
    }

if __name__ == "__main__":
    app.run(debug=True)