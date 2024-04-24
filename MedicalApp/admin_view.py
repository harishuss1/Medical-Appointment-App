from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .db.dbmanager import get_db
from .user import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@login_required
def add_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        avatar_path = request.form.get('avatar_path')
        user_type = request.form['user_type']

        new_user = User(email, password, first_name, last_name, user_type, avatar_path)
        
        db = get_db()
        try:
            db.create_user(new_user)
            flash("User created successfully!")
            return redirect(url_for('admin_view.admin_dashboard'))
        except Exception as e:
            flash(f"Error creating user: {e}")
    
    return render_template('add_user.html')

# Delete User Route
@admin_bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        try:
            db.delete_user(email)
            flash("User deleted successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error deleting user: {e}", 'error')
    
    return render_template('delete_user.html')

@login_required
def block_user():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        try:
            db.block_user(email)
            flash("User blocked successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error blocking user: {e}", 'error')
    
    return render_template('block_user.html')

@admin_bp.route('/change_user_role', methods=['GET', 'POST'])
@login_required
def change_user_role():
    if request.method == 'POST':
        email = request.form['email']
        new_user_type = request.form['user_type']
        
        db = get_db()
        try:
            db.change_user_type(email, new_user_type)
            flash("User role changed successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error changing user role: {e}", 'error')
    
    return render_template('change_user_role.html')


