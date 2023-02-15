from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.login import LogIn
from App.models import User

profile_views = Blueprint('profile_views', __name__, template_folder='../templates')


@profile_views.route('/profile', methods=['GET'])
@login_required
def index_page():
    return render_template('profile.html')