import json
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db

bp = Blueprint('users', __name__, url_prefix="/users/")

def highest_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'ADMIN':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('/roles/')
@login_required
@highest_access
def users_roles():
    try:
        users = get_db().get_users_and_roles()
        
        if users is None or len(users) == 0:
            flash("There are no users in the database")
            return redirect(url_for('home.index'))
    except DatabaseError as e:
        flash('An error occured with the database')
        return redirect(url_for('home.index'))
    except ValueError as e: 
        flash("Incorrect values were passed")
        return redirect(url_for('home.index'))
    return render_template('users.html', users=users)