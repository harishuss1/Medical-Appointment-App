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
from .forms import AddAttachementForm, NoteForm
from .db.db import Database
from .note import Note

bp = Blueprint('note', __name__, url_prefix="/notes/")


def doctor_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@bp.route('/<int:note_id>/', methods=['GET', 'POST'])
@login_required
@doctor_access
def note(note_id):
    form = AddAttachementForm()
    note = None
    try:
        note = get_db().get_note_by_id(note_id)
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect(url_for('home.index'))

    if note == None:
        flash("no note available")
        return redirect(url_for('note.notes', user_id=current_user.id))

    if request.method == 'POST' and form.validate_on_submit():
        files = form.attachement.data
        paths = []
        for file in files:
            filename = file.filename
            folder = os.path.join(
                current_app.config['ATTACHEMENTS'], str(note.patient.id))
            if not os.path.exists(folder):
                os.makedirs(folder)
            path = os.path.join(folder, filename)
            path = os.path.relpath(path, start=os.curdir)
            paths.append(path)
            file.save(path)
        try:
            get_db().update_note(note, paths)
        except DatabaseError as e:
            flash("Something went wrong with the database")
            return redirect(url_for('home.index'))
        except TypeError as e:
            flash("Incorrect types sent")
            return redirect(url_for('home.index'))
            
    return render_template('note.html', note=note, form=form)


@bp.route('/note/<int:user_id>/')
@login_required
@doctor_access
def notes(user_id):
    notes = None
    try:
        if current_user.access_level == 'STAFF':
            notes = get_db().get_notes_by_doctor_id(user_id)
        else:
            notes = get_db().get_notes_by_patient_id(user_id)
        if notes is None or len(notes) == 0:
            flash("No notes are currently written for this user")
            return redirect(url_for('doctor.dashboard'))
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))
    return render_template('notes.html', notes=notes)


@bp.route('/add/', methods=['GET', 'POST'])
@login_required
@doctor_access
def add():
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
        try:
            patient = get_db().get_patients_by_id(form.patient.data)
            # form.date.data.strftime('%Y-%m-%d')
            note = Note(patient, current_user,
                        form.date.data, form.note.data, paths)
            get_db().create_note(note)
            return redirect(url_for('note.notes', user_id=current_user.id))
        except DatabaseError as e:
            flash("something went wrong with the database")
        except ValueError as e:
            flash("Incorrect values were passed")
    return render_template('add_note.html', form=form)

# source: https://stackoverflow.com/questions/27337013/how-to-send-zip-files-in-the-python-flask-framework


@bp.route('/note/<int:note_id>/attachments/', methods=['GET', 'POST'])
@login_required
@doctor_access
def get_attachments(note_id):
    try:
        attachments = get_db().get_attachements_by_note_id(note_id)

        if attachments is None or len(attachments) == 0:
            flash("this user has no attachements")

        buffer = io.BytesIO()

        # Create a ZipFile object with the BytesIO buffer
        with ZipFile(buffer, 'w') as zipf:
            for attachment in attachments:
                # Add attachment to zip archive
                try:
                    zipf.write(attachment, os.path.basename(attachment))
                except FileNotFoundError as e:
                    continue

        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name='attachements.zip', mimetype='application/zip')
    
    except DatabaseError as e:
        flash("something went wrong with obtaining attachements")
        return redirect(url_for('note.note', note_id=note_id))
