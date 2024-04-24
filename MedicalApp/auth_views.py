from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
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
        user = User(form.first_name, form.last_name, form.email.data, pwd_hash)
        get_db().create_user(user)
        redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

# Change the templates once they are completed


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = get_db().get_user_by_email(form.email.data)
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            return redirect(url_for('home.index'))
        else:
            flash('Incorrect info')
    return render_template('login.html', form=form)
