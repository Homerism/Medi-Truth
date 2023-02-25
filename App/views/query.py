from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash, url_for
from flask_login import login_user, login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import User

query_views = Blueprint('query_views', __name__, template_folder='../templates')

from App.controllers import (
    health_classification,
    most_frequent_word
)

@query_views.route('/query', methods=['GET'])
@login_required
def index_page():
    form = QueryForm()
    return render_template('profile.html', form=form)


@query_views.route('/query', methods=['POST'])
@login_required
def queryAction():
    form = QueryForm()
    if form.validate:
       prediction = health_classification(form.textarea.data)
       word = most_frequent_word(form.textarea.data)
       flash(f" {prediction} this is the prediction....this is the word {word}")
       return redirect(url_for('query_views.queryAction'))
    return render_template('profile.html', form=form)