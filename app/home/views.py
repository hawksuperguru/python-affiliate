from flask import render_template, url_for, redirect
from flask_login import login_required
from . import home_app as home
from ..models import Affiliate, History, db
from pprint import pprint

import datetime

def get_delta_date(delta = 2, format_string = "%Y/%m/%d"):
    today = datetime.datetime.today()
    diff = datetime.timedelta(days = delta)
    return (today - diff).strftime(format_string)

@home.route('/')
@login_required
def homepage():
    """
    Render the home page template on the / route
    """
    return redirect(url_for('home.dashboard'))
    # return render_template("home/dashboard.html", title = "Dashbaord")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    render the dashboard.
    """
    initial_date = get_delta_date()
    histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
    .add_columns(Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
    History.weekly_click, History.weekly_signup, History.weekly_commission, \
    History.monthly_click, History.monthly_signup, History.monthly_commission, \
    History.yearly_click, History.yearly_signup, History.yearly_commission, \
    History.paid_signup, History.created_at)\
    .filter(History.created_at == initial_date).all()
    print("======================   Here    ====================")
    pprint(histories[0].monthly_commission)
    print("===========================================")
    return render_template("home/dashboard.html", title = "Dashbaord", histories = histories)