import os
from flask import (Blueprint, current_app, render_template, redirect,
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
    if current_user.access_level != 'STAFF' and current_user.access_level != 'PATIENT':
        return redirect(url_for('home.index'))
    notes = None
    try:
        #<dd><a href="{{ url_for('note.notes', user_id=patient.id) }}">See notes.</a></dd> what to do about this...
        #CHANGE TO RELATIVE PATH
        if current_user.access_level == 'STAFF':
            notes = get_db().get_notes_by_doctor_id(user_id)
        else:
            notes = get_db().get_notes_by_patient_id(user_id)
        if notes is None or len(notes) == 0:
            flash("No notes are currently written for this user")
    except DatabaseError as e:
        flash("Something went wrong with the database")
    return render_template('notes.html', notes=notes)
    
@bp.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.access_level != 'STAFF':
        return redirect('home.index')
    form = NoteForm()
    form.set_choices()
    if request.method == 'POST' and form.validate_on_submit():
        file = form.attachement.data
        filename = file.filename
        folder = os.path.join(current_app.config['ATTACHEMENTS'], form.patient.data)
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = os.path.join(folder, filename)
        path = os.path.relpath(path, start=os.curdir) #??? from what starting directory should we be?
        file.save(path)
        
        patient = get_db().get_patients_by_id(form.patient.data)
        #form.date.data.strftime('%Y-%m-%d')
        note = Note(patient, current_user, form.date.data, form.note.data, path)
        
        get_db().create_note(note)
        return redirect(url_for('note.notes', user_id=current_user.id))
    return render_template('add_note.html', form=form)