from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date, datetime
from ch_100_app.models import User

# from ch_100_app.main.forms import

# Import app and db from events_app package so that we can run app
from ch_100_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    return render_template("home.html")
