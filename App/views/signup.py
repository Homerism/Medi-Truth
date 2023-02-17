from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.signup import SignUp
from App.models import User

from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
)

signup_views = Blueprint('signup_views', __name__, template_folder='../templates')

@signup_views.route('/signup', methods=['GET'])
def signupIndex():
  form = SignUp()
  return render_template('signup.html', form=form)

@signup_views.route('/signup', methods=['POST'])
def signupAction():
    form = SignUp()
    if form.validate:
       create_user(form.username.data, form.password.data)
       flash(f"User {form.username.data} created!")
       return redirect(url_for('login_views.loginIndex'))
    return "Abort"