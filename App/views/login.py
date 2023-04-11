from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_user, login_required, logout_user
from App.database import db
from App.forms.login import LogIn
from App.models import User

login_views = Blueprint('login_views', __name__,
                        template_folder='../templates')


@login_views.route('/login', methods=['GET'])
def loginIndex():
    return render_template('login.html')


@login_views.route('/login', methods=['POST'])
def loginAction():
    username = request.form.get("username")
    password = request.form.get("password")
    error = ""
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return redirect(url_for('query_views.index_page'))
    error = "Incorrect Password Input"
    return render_template('login.html', error=error)


@login_views.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_views.index'))
