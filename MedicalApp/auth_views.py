from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from MedicalApp.db.dbmanager import get_db
from MedicalApp.forms import LoginForm, SignupForm
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

# Change the templates once they are completed


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = get_db().get_user_by_email(form.email.data)
        if user is not None and check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            if current_user.access_level == 'STAFF':
                return redirect(url_for('doctor.dashboard'))
            return redirect(url_for('home.index'))
        else:
            flash('Incorrect info')
    return render_template('login.html', form=form)
