import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_user, login_required, logout_user
from oracledb import DatabaseError, IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from MedicalApp.db.dbmanager import get_db
from MedicalApp.forms import AvatarForm, LoginForm, SignupForm, ChangePasswordForm
from MedicalApp.user import User

import secrets
from werkzeug.utils import secure_filename


bp = Blueprint('auth', __name__, url_prefix='/auth/')


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        pwd_hash = generate_password_hash(form.password.data)
        user = User(form.email.data, pwd_hash,
                    form.first_name.data, form.last_name.data)
        try:
            get_db().create_user(user)
        except IntegrityError as e:
            flash("This email already exists")
            return redirect('auth.signup')
        except DatabaseError as e:
            flash("Something went wrong with the database")
            return redirect('auth.signup')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = get_db().get_user_by_email(form.email.data)
        except DatabaseError as e:
            flash("something went wrong with the database")
            return redirect('home.index')
        except ValueError as e: 
            flash("Incorrect values were passed")
            return redirect('home.index')
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            if current_user.access_level == 'STAFF':
                return redirect(url_for('doctor.dashboard'))
            if current_user.access_level == 'BLOCKED':
                flash("Adminstrators has blocked this account.", "error")
            if current_user.access_level in ('ADMIN', 'ADMIN_USER'):
                return redirect(url_for('admin.admin_dashboard'))
            return redirect(url_for('home.index'))
        else:
            flash('Incorrect info')
    return render_template('login.html', form=form)


@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Succesfully Logged out!")
    return redirect(url_for('auth.login'))


@bp.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    form = AvatarForm()

    if request.method == 'POST' and form.validate_on_submit():
        if form.avatar.data:
            avatar_file = form.avatar.data
            filename = avatar_file.filename
            folder = os.path.join(
                current_app.config['IMAGES'], current_user.email)
            if not os.path.exists(folder):
                os.makedirs(folder)
            avatar_path = os.path.join(folder, filename)
            avatar_file.save(avatar_path)

            # Convert the absolute path to a relative path
            relative_path = os.path.relpath(avatar_path, start=os.curdir)
            current_user.avatar_path = relative_path
            try:
                db = get_db()
                db.update_user_avatar(current_user.id, relative_path)
                flash("Avatar updated successfully.", "success")
                return redirect(url_for("auth.profile"))
            except DatabaseError as e:
                flash("Something went wrong with the database")
                return redirect(url_for('home.index'))
            except ValueError as e: 
                flash("Incorrect values were passed")
                return redirect(url_for('home.index'))
        else:
            flash("No file was submitted.", "error")
    return render_template("profile.html", form=form, current_user=current_user)


@bp.route('/profile/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            if not check_password_hash(current_user.password, form.current_password.data):
                flash("Current password is incorrect.", "error")
                return redirect(render_template("profile.html", form=form))

            new_password_hash = generate_password_hash(form.new_password.data)
            current_user.password = new_password_hash
            db = get_db()
            db.update_user_password(current_user.id, new_password_hash)
            flash("Password changed successfully.", "success")
            return redirect(url_for("auth.profile"))
        except DatabaseError as e:
                flash("Something went wrong with the database")
        except ValueError as e: 
            flash("Incorrect values were passed")
    return render_template("profile.html", form=form, current_user=current_user)


@bp.route('/profile/<email>/<filename>')
@login_required
def get_avatar(email, filename):
    return send_from_directory(os.path.join(current_app.config['IMAGES'], email), filename)

@bp.route('/profile/userApiToken/', methods=['GET'])
@login_required
def user_api_token():
    api_token = secrets.token_urlsafe(20)
    return render_template('user_api_token.html', api_token=api_token)