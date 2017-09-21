from flask import render_template, url_for, redirect, request, jsonify
from sqlalchemy import func
from flask_login import login_required
from . import home_app as home
from ..models import Affiliate, History, db
from pprint import pprint

import datetime, json

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

STATISTIC_COMPUTING_METHOD = 'temp'

def get_weekly_histories():
    if STATISTIC_COMPUTING_METHOD == 'temp':
        initial_date = get_delta_date()
        histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
            .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
            History.weekly_click, History.weekly_signup, History.weekly_commission, \
            History.monthly_click, History.monthly_signup, History.monthly_commission, \
            History.yearly_click, History.yearly_signup, History.yearly_commission, \
            History.paid_signup, History.created_at)\
            .filter(History.created_at == initial_date).all()
        return histories

    else:
        start_date = get_delta_date(9)
        end_date = get_delta_date(2)
        histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
            .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
            History.weekly_click, History.weekly_signup, History.weekly_commission, \
            History.monthly_click, History.monthly_signup, History.monthly_commission, \
            History.yearly_click, History.yearly_signup, History.yearly_commission, \
            History.paid_signup, History.created_at)\
            .filter(History.created_at >= start_date)\
            .filter(History.created_at <= end_date).all()
        
        return histories

def get_monthly_histories():
    if STATISTIC_COMPUTING_METHOD == 'temp':
        initial_date = get_delta_date()
        histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
            .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
            History.weekly_click, History.weekly_signup, History.weekly_commission, \
            History.monthly_click, History.monthly_signup, History.monthly_commission, \
            History.yearly_click, History.yearly_signup, History.yearly_commission, \
            History.paid_signup, History.created_at)\
            .filter(History.created_at == initial_date).all()
        return histories
    else:
        start_date = get_delta_date(9)
        end_date = get_delta_date(2)
        histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
            .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
            History.weekly_click, History.weekly_signup, History.weekly_commission, \
            History.monthly_click, History.monthly_signup, History.monthly_commission, \
            History.yearly_click, History.yearly_signup, History.yearly_commission, \
            History.paid_signup, History.created_at)\
            .filter(History.created_at >= start_date)\
            .filter(History.created_at <= end_date).all()
        
        return histories

def get_yearly_histories():
    if STATISTIC_COMPUTING_METHOD == 'temp':
        initial_date = get_delta_date()
        histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
            .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
            History.weekly_click, History.weekly_signup, History.weekly_commission, \
            History.monthly_click, History.monthly_signup, History.monthly_commission, \
            History.yearly_click, History.yearly_signup, History.yearly_commission, \
            History.paid_signup, History.created_at)\
            .filter(History.created_at == initial_date).all()
        return histories
    else:
        start_date = get_delta_date(9)
        end_date = get_delta_date(2)
        histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
            .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
            History.weekly_click, History.weekly_signup, History.weekly_commission, \
            History.monthly_click, History.monthly_signup, History.monthly_commission, \
            History.yearly_click, History.yearly_signup, History.yearly_commission, \
            History.paid_signup, History.created_at)\
            .filter(History.created_at >= start_date)\
            .filter(History.created_at <= end_date).all()
        
        return histories

def get_from_date_range(start, end):
    # histories = db.session.query()
    histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
        .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
        History.weekly_click, History.weekly_signup, History.weekly_commission, \
        History.monthly_click, History.monthly_signup, History.monthly_commission, \
        History.yearly_click, History.yearly_signup, History.yearly_commission, \
        History.paid_signup, History.created_at)\
        .filter(History.created_at >= start)\
        .filter(History.created_at <= end).all()

def get_histories(mode, range = None):
    if mode == 'daily':
        initial_date = get_delta_date()
        histories = History.query.join(Affiliate, Affiliate.id == History.affiliate_id)\
            .add_columns(History.affiliate_id, Affiliate.name, History.daily_click, History.daily_signup, History.daily_commission, \
            History.weekly_click, History.weekly_signup, History.weekly_commission, \
            History.monthly_click, History.monthly_signup, History.monthly_commission, \
            History.yearly_click, History.yearly_signup, History.yearly_commission, \
            History.paid_signup, History.created_at)\
            .filter(History.created_at == initial_date).all()
        return histories
    elif mode == 'weekly':
        return get_weekly_histories()
    elif mode == "monthly":
        return get_monthly_histories()
    elif mode == "yearly":
        return get_yearly_histories()
    else:
        if range is None:
            initial_date = get_delta_date(2, '%Y-%m-%d')
            range = "{} - {}".format(initial_date, initial_date)
        
        [start, end] = range.split(" - ")
        return get_from_date_range(start, end)


@home.route('/dashboard')
@login_required
def dashboard():
    """
    render the dashboard.
    """
    initial_date = get_delta_date()
    histories = get_histories('daily')
    return render_template("home/dashboard.html", title = "Dashbaord", date = initial_date, histories = histories)


@home.route('/histories', methods = ['POST', 'GET'])
def api_histories():
    mode = request.args.get('mode')
    date_range = user = request.args.get('date_range')
    histories = []

    for history in get_histories(mode, date_range):
        histories.append({
            'id': history.affiliate_id,
            'name': history.name,
            'daily_click': history.daily_click,
            'daily_signup': history.daily_signup,
            'daily_commission': history.daily_commission,
            'weekly_click': history.weekly_click,
            'weekly_signup': history.weekly_signup,
            'weekly_commission': history.weekly_commission,
            'monthly_click': history.monthly_click,
            'monthly_signup': history.monthly_signup,
            'monthly_commission': history.monthly_commission,
            'yearly_click': history.yearly_click,
            'yearly_signup': history.yearly_signup,
            'yearly_commission': history.yearly_commission,
            'paid_signup': history.paid_signup,
            'created_at': history.created_at
        })
    return jsonify(status = True, histories = histories)