from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.login import LogIn
from App.models import User

login_views = Blueprint('login_views', __name__, template_folder='../templates')




@login_views.route('/login', methods=['GET', 'POST'])
def get_login_page():
    if request.method == 'POST':
        form = LogIn()
        if form.validate_on_submit():
            data = request.form
            user = User.query.filter_by(username=data['username']).first()
            if user and user.check_password(data['password']):
                login_user(user)
                return redirect(url_for('profile_views.get_user_page'))    
        flash('Invalid credentials')
        return redirect(url_for('login_views.get_user_page'))
    else:
        form = LogIn()
        return render_template('login.html', form=form)

# @login_views.route('/login', methods=['POST'])
# def login_current_user():
#     form = LogIn()
#     if form.validate_on_submit():
#         data = request.form
#         user = User.query.filter_by(username=data['username']).first()
#         if user and user.check_password(data['password']):
#             login_user(user)
#             return redirect(url_for('index_views.get_user_page'))
#     flash('Invalid credentials')
#     return redirect(url_for('login_views.login_current_user'))  