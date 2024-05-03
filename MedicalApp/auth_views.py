from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from MedicalApp.db.dbmanager import get_db
from MedicalApp.forms import LoginForm, SignupForm, ChangePasswordForm
from MedicalApp.user import User


bp = Blueprint('auth', __name__, url_prefix='/auth/')


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        pwd_hash = generate_password_hash(form.password.data)
        user = User(form.email.data, pwd_hash,
                    form.first_name.data, form.last_name.data)
        get_db().create_user(user)
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = get_db().get_user_by_email(form.email.data)
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            if current_user.access_level == 'STAFF':
                return redirect(url_for('doctor.dashboard'))
            if current_user.access_level == 'BLOCKED':
                flash("Adminstrators has blocked this account.", "error")
                #use logout() needs to be implemented
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
    form = ChangePasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        if not check_password_hash(current_user.password, form.current_password.data):
            flash("Current password is incorrect.", "error")
            return render_template("profile.html", form=form)


        new_password_hash = generate_password_hash(form.new_password.data)
        current_user.password = new_password_hash
        db = get_db()
        db.update_user_password(current_user.id, new_password_hash)
        flash("Password changed successfully.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("profile.html", form=form, current_user=current_user)