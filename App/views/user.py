from flask import Blueprint, redirect, render_template, request, jsonify, send_from_directory, flash, url_for
from flask_login import current_user, login_required
user_views = Blueprint('user_views', __name__, template_folder='../templates')
from App.models import User
from App.controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
def profile_page():
    users = get_all_users
    return render_template('users.html', users=users)