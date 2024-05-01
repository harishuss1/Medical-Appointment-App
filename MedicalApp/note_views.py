import io
import os
import shutil
import tempfile
from zipfile import ZipFile
from flask import (Blueprint, after_this_request, current_app, render_template, redirect,
                   flash, send_file, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError
from flask_login import current_user, login_user, logout_user, login_required
from .forms import NoteForm
from .db.db import Database
from .note import Note

bp = Blueprint('note', __name__, url_prefix="/notes/")

def doctor_access(func):
    def wrapper():
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func()
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('/<int:note_id>/')
@login_required
@doctor_access
def note(note_id):
    note = get_db().get_note_by_id(note_id)
    if note == None:
        flash("no note available")
        return redirect(url_for('note.notes', user_id=current_user.id))
    return render_template('note.html', note=note)


@bp.route('/note/<int:user_id>/')
@login_required
@doctor_access
def notes(user_id):
    if current_user.access_level != 'STAFF' and current_user.access_level != 'PATIENT':
        return redirect(url_for('home.index'))
    notes = None
    try:
        # <dd><a href="{{ url_for('note.notes', user_id=patient.id) }}">See notes.</a></dd> what to do about this...
        # CHANGE TO RELATIVE PATH
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
@doctor_access
def add():
    if current_user.access_level != 'STAFF':
        return redirect('home.index')
    form = NoteForm()
    form.set_choices()
    if request.method == 'POST' and form.validate_on_submit():
        files = form.attachement.data
        paths = []
        for file in files:
            filename = file.filename
            folder = os.path.join(
                current_app.config['ATTACHEMENTS'], form.patient.data)
            if not os.path.exists(folder):
                os.makedirs(folder)
            path = os.path.join(folder, filename)
            path = os.path.relpath(path, start=os.curdir)
            paths.append(path)
            file.save(path)  # actually adds it to the directory

        patient = get_db().get_patients_by_id(form.patient.data)
        # form.date.data.strftime('%Y-%m-%d')
        note = Note(patient, current_user,
                    form.date.data, form.note.data, paths)

        get_db().create_note(note)
        return redirect(url_for('note.notes', user_id=current_user.id))
    return render_template('add_note.html', form=form)

# source: https://stackoverflow.com/questions/27337013/how-to-send-zip-files-in-the-python-flask-framework


@bp.route('/note/<int:note_id>/attachments/', methods=['GET', 'POST'])
@login_required
@doctor_access
def get_attachments(note_id):
    attachments = get_db().get_attachements_by_note_id(note_id)
    buffer = io.BytesIO()

    # Create a ZipFile object with the BytesIO buffer
    with ZipFile(buffer, 'w') as zipf:
        for attachment in attachments:
            # Add attachment to zip archive
            zipf.write(attachment, os.path.basename(attachment))

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='attachements.zip', mimetype='application/zip')
