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
    username = request.form.get("username")
    password = request.form.get("password")
    npi = request.form.get("npi")
    error = ""

    real_npi = check_npi(npi)
    if not real_npi:
        error = "This is an invalid NPI number"
        return render_template('doctorsignup.html', error=error)

    npi_referral = get_npi_number(npi)
    if not npi_referral:
        error = "This is an invalid NPI number"
        return render_template('doctorsignup.html', error=error)

    create_user(username, 'Doctor', password)
    return redirect(url_for('login_views.loginIndex'))
