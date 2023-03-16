from flask import Blueprint,render_template, request, flash
from flask_login import login_required, current_user 
from App.database import db
from App.forms.query import QueryForm
from App.models import ArticleRate

feed_views = Blueprint('feed_views', __name__, template_folder='../templates')

from App.controllers import create_article_for_doctors

@feed_views.route('/feed', methods=['GET'])
@login_required
def index_page():
    doctorArticles = ArticleRate.query.all()
    return render_template('doctorFeed.html', articles=doctorArticles)