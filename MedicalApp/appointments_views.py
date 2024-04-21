"""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from MedicalApp.appointments import AddressForm, Address
from AddressApp import db, dbmanager

bp = Blueprint('appointments', __name__, url_prefix='/appointments/')


@bp.route('', methods=['GET', 'POST'])
def get_appointments():
    db = dbmanager.get_db()
    appointments = db.get_appointments()
    if appointments is None or len(appointments) == 0:
        abort(404)

    form = AppointmentsForm()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        street = form.street.data
        city = form.city.data
        province = form.province.data
        new_address = Address(name, street, city, province)

        # checks if theres any existing address in the addresses list and it will check if it matches with
        # the new address, if match then it flashed that it already exist and
        # will not take the new address
        if any(address.name == new_address.name and
               address.street == new_address.street and
               address.city == new_address.city and
               address.province == new_address.province
               for address in addresses):
            flash("Address already exists", "error")
        else:
            new_address = Address(name, street, city, province)
            db.add_address(new_address)
            flash("Address added to the List of Address")

            return redirect(
                url_for('addressbook.get_address', name=new_address.name))

    return render_template('addresses.html', addresses=addresses, form=form)


@bp.route('/<string:name>/')
def get_address(name):
    db = dbmanager.get_db()
    address = db.get_address(name)
    if address is None:
        flash("Address cannot be found", 'error')
        return redirect(url_for('addressbook.address_list'))
    return render_template('specific_address.html', address=address)
"""
