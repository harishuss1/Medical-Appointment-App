from flask import Blueprint, abort, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user, login_user, logout_user
from oracledb import DatabaseError
from .db.dbmanager import get_db
from .user import User
from .db.db import Database
from .forms import AddUserForm, DeleteUserForm, ChangeUserRoleForm, BlockUserForm
from werkzeug.security import generate_password_hash


admin_bp = Blueprint('admin', __name__, url_prefix='/admin/')

def admin_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def highest_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'ADMIN':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@admin_bp.route('/')
@login_required
@admin_access
def admin_dashboard():
    try:
        users = get_db().get_users_and_roles()
        
        if users is None or len(users) == 0:
            flash("There are no users in the database")
            return redirect(url_for('home.index'))
        return render_template('admin_dashboard.html', users=users)
    except DatabaseError as e:
        flash('An error occured with the database')
        return redirect(url_for('home.index'))
    except ValueError as e: 
        flash("Incorrect values were passed")
        return redirect(url_for('home.index'))


@admin_bp.route('/add_user/', methods=['GET', 'POST'])
@login_required
@admin_access
def add_user():
    form = AddUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        pwd_hash = generate_password_hash(form.password.data)
        first_name = form.first_name.data
        last_name = form.last_name.data
        avatar_path = form.avatar_path.data or None
        user_type = form.user_type.data

        new_user = User(email, pwd_hash, first_name,
                        last_name, user_type, avatar_path)

        db = get_db()
        try:
            db.create_user(new_user)
            flash("User created successfully!", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error creating user: {e}", 'error')

    return render_template('add_user.html', form=form)


@admin_bp.route('/delete_user/<string:email>/', methods=['GET', 'POST'])
@login_required
@admin_access
def delete_user(email):
    form = DeleteUserForm()
    form.email.data = email
    form.email.render_kw = {'disabled': ''}
    if request.method == 'POST' and form.validate_on_submit():
        user_delete = form.email.data
        user = get_db().get_user_by_email(user_delete)
        db = get_db()
        try:
            db.delete_user(user_delete)
            flash("User deleted successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"This user is not valid", 'error')
    return render_template('delete_user.html', form=form)


@admin_bp.route('/block_user/<string:email>/', methods=['GET', 'POST'])
@login_required
@admin_access
def block_user(email):
    if current_user.access_level not in ('ADMIN', 'ADMIN_USER'):
        return redirect(url_for('home.index'))
    form = BlockUserForm()
    form.email.data = email
    form.email.render_kw = {'disabled': ''}
    if request.method == 'POST' and form.validate_on_submit():
        user_delete = form.email.data
        db = get_db()
        try:
            db.block_user(user_delete)
            flash("User blocked successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"This user is not valid", 'error')

    return render_template('block_user.html', form=form)


# only ADMIN can do this one
@admin_bp.route('/change_user_role/<string:email>/', methods=['GET', 'POST'])
@login_required
@highest_access
def change_user_role(email):
    if current_user.access_level != 'ADMIN':
        return redirect(url_for('home.index'))
    form = ChangeUserRoleForm()
    form.email.data = email
    form.email.render_kw = {'disabled': ''}
    if request.method == 'POST' and form.validate_on_submit():
        user_delete = form.email.data
        new_user_type = form.user_type.data

        db = get_db()
        try:
            db.change_user_type(user_delete, new_user_type)
            flash("User role changed successfully", 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            flash(f"Error changing user role: {e}", 'error')

    return render_template('change_user_role.html', form=form)
