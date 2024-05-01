from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from .db.dbmanager import get_db
from .user import User
from .db.db import Database
from .forms import AddUserForm, DeleteUserForm, ChangeUserRoleForm, BlockUserForm
from werkzeug.security import generate_password_hash


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if current_user.access_level not in ('ADMIN', 'ADMIN_USER'):
        return redirect(url_for('home.index'))
    user = current_user if current_user.is_authenticated else None
    return render_template('admin_dashboard.html', user=user)


@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.access_level not in ('ADMIN', 'ADMIN_USER'):
        return redirect(url_for('home.index'))
    form = AddUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        pwd_hash = generate_password_hash(form.password.data)
        first_name = form.first_name.data
        last_name = form.last_name.data
        avatar_path = form.avatar_path.data or None
        user_type = form.user_type.data
        
        new_user = User(email, pwd_hash, first_name, last_name, user_type, avatar_path)
        
        db = get_db()
        try:
            db.create_user(new_user)
            flash("User created successfully!", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error creating user: {e}", 'error')
    
    return render_template('add_user.html', form=form)


@admin_bp.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    if current_user.access_level not in ('ADMIN', 'ADMIN_USER'):
        return redirect(url_for('home.index'))
    form = DeleteUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        db = get_db()
        try:
            db.delete_user(email)
            flash("User deleted successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error deleting user: {e}", 'error') 
    return render_template('delete_user.html', form=form)


@admin_bp.route('/block_user', methods=['GET', 'POST'])
@login_required
def block_user():
    if current_user.access_level not in ('ADMIN', 'ADMIN_USER'):
        return redirect(url_for('home.index'))
    form = BlockUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        db = get_db()
        try:
            db.block_user(email)
            flash("User blocked successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error blocking user: {e}", 'error')
    
    return render_template('block_user.html', form=form)


# only ADMIN can do this one
@admin_bp.route('/change_user_role', methods=['GET', 'POST'])
@login_required
def change_user_role():
    if current_user.access_level != 'ADMIN':
        return redirect(url_for('home.index'))
    form = ChangeUserRoleForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        new_user_type = form.user_type.data
        
        db = get_db()
        try:
            db.change_user_type(email, new_user_type)
            flash("User role changed successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error changing user role: {e}", 'error')
    
    return render_template('change_user_role.html', form=form)
