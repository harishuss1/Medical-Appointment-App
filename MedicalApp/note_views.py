from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError
from flask_login import current_user, login_user, logout_user, login_required
from .forms import NoteForm
from .db.db import Database
from .note import Note

bp = Blueprint('note', __name__, url_prefix="/notes/")


@bp.route('/<int:user_id>/')
@login_required
def notes(user_id):
    if current_user.access_level != 'STAFF' or current_user.access_level != 'PATIENT':
        return redirect(url_for('home.index'))
    try:
        notes = get_db().get_notes_by_patient_id(user_id)
        if notes is None or len(notes) == 0:
            flash("No notes are currently written for this patient")
            return redirect(url_for('doctor.dashboard'))
        return render_template('notes.html', notes=notes)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))
    
@bp.route('/add/', methods=['GET', 'POST'])
def add(user_id):
    form = NoteForm()
    if request.method == 'POST' and form.validate_on_submit():
        note = Note()