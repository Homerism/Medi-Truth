from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from datetime import datetime
import random
import csv

feedback_views = Blueprint('feedback_views', __name__, template_folder='../templates')

from App.controllers.algorithm import (
    data_in_csv_check
)

@feedback_views.route("/feedback", methods=["GET", "POST"])
@login_required
def index():
    error = ""
    if request.method == 'POST':
        id = random.randint(0,100000)
        name = current_user.username
        statement = request.form['statement'].strip()
        description = request.form['description']
        category = "medical/health"
        rating = request.form['rating']
        queries = "null"
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updated_at = created_at
        found = data_in_csv_check(statement)
        if not found:
            with open('App/controllers/claims.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([id, name, statement, description, category, rating, queries, created_at, updated_at])
                error+=f"feedback sucessfully added. Thank you for your contribution!{found}"
                return render_template("feedback.html",error=error)
        else:
            error+=f"Seems there is this claim already in our dataset, try rewording and submit again, thank you.{found}"
            return render_template("feedback.html", error=error)
    else:
        return render_template("feedback.html",error=error)
