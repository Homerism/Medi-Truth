from flask import Blueprint, redirect, render_template, flash, request, url_for
from App.database import db
from App.forms.usersignup import UserSignUp
from App.forms.doctorsignup import DoctorSignUp

from App.controllers import (
    create_user,
    get_npi_number,
    check_npi
)

signup_views = Blueprint('signup_views', __name__,
                         template_folder='../templates')

# <----------------------User SIGNUP----------------------------------->


@signup_views.route('/usersignup', methods=['GET'])
def UserSignupIndex():
    return render_template('usersignup.html')


@signup_views.route('/usersignup', methods=['POST'])
def UserSignupAction():
    username = request.form.get("username")
    password = request.form.get("password")
    error = ""
    create_user(username, 'General User', password)
    return redirect(url_for('login_views.loginIndex'))

# <----------------------DOCTOR SIGNUP----------------------------------->


@signup_views.route('/doctorsignup', methods=['GET'])
def DoctorSignupIndex():
    form = DoctorSignUp()
    return render_template('doctorsignup.html', form=form)


@signup_views.route('/doctorsignup', methods=['POST'])
def DoctorSignupAction():
    form = DoctorSignUp()
    error = ""
    if form.validate:
        real_npi = check_npi(form.npi.data)
        if not real_npi:
            error = "This is an invalid NPI number"
            return render_template('doctorsignup.html', form=form, error=error)

        npi = get_npi_number(form.npi.data)
        if not npi:
            error = "This is an invalid NPI number"
            return render_template('doctorsignup.html', form=form, error=error)

        create_user(form.username.data, 'Doctor', form.password.data)
        flash(f"User {form.username.data} created!")
        return redirect(url_for('login_views.loginIndex'))
