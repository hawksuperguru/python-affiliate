from flask import render_template
from flask_login import login_required
from . import home_app as home

@home.route('/')
@login_required
def homepage():
    """
    Render the home page template on the / route
    """
    return render_template("home/dashboard.html", title = "Dashbaord")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    render the dashboard.
    """
    return render_template("home/dashboard.html", title = "Dashbaord")