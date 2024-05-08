import json
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db

bp = Blueprint('allergy_api', __name__, url_prefix="/api/allergies/")