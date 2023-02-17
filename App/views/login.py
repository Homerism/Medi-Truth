from flask import Blueprint, redirect, render_template, flash, url_for
from flask_login import login_user, login_required, logout_user 
from App.database import db
from App.forms.login import LogIn
from App.models import User

login_views = Blueprint('login_views', __name__, template_folder='../templates')

@login_views.route('/login', methods=['GET'])
def loginIndex():
  form = LogIn()
  return render_template('login.html', form=form)

@login_views.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  error = ""
  if form.validate:
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
      login_user(user)
      flash(f"User {form.username.data} has logged in successfully!")
      return redirect(url_for('profile_views.index_page'))
    error = "Incorrect Password Input"
    return render_template('login.html', form=form, error=error)

@login_views.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return redirect(url_for('index_views.index'))