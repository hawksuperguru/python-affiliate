from flask import render_template, url_for, redirect, request, jsonify
from sqlalchemy import func
from flask_login import login_required
from . import home_app as home
from ..models import Affiliate, History, db
from pprint import pprint
from .. import get_issues

import datetime, json
import dateutil.relativedelta

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
    start_date = get_delta_date(9)
    end_date = get_delta_date(2)
    
    return get_from_date_range(start_date, end_date)

def get_monthly_histories():
    today = datetime.datetime.today()
    diff = datetime.timedelta(days = 2)
    end_date = (today - diff)#.strftime("%Y/%m/%d")

    delta = dateutil.relativedelta.relativedelta(months = 1)
    start_date = end_date - delta

    return get_from_date_range(start_date.strftime("%Y/%m/%d"), end_date.strftime("%Y/%m/%d"))

def get_yearly_histories():
    today = datetime.datetime.today()
    diff = datetime.timedelta(days = 2)
    end_date = (today - diff)#.strftime("%Y/%m/%d")

    delta = dateutil.relativedelta.relativedelta(years = 1)
    start_date = end_date - delta

    return get_from_date_range(start_date.strftime("%Y/%m/%d"), end_date.strftime("%Y/%m/%d"))

def get_from_date_range(start, end):
    histories = db.session.query(
        Affiliate.id,
        Affiliate.name,
        func.sum(History.daily_click).label('click'),
        func.sum(History.daily_signup).label('signup'),
        func.sum(History.daily_commission).label('commission'),
        func.sum(History.rate).label('rate'),
    ).filter(
        History.created_at >= start,
        History.created_at <= end
    ).join(History.affiliate).group_by(Affiliate.id).order_by('rate desc').all()

    results = []
    for history in histories:
        last_history = History.query.filter(
            History.affiliate_id == history.id,
            History.created_at >= start,
            History.created_at <= end
        ).order_by(History.created_at.desc()).first()

        results.append({
            'id': history.id,
            'name': history.name,
            'click': history.click,
            'signup': history.signup,
            'commission': history.commission,
            'affiliate_click': last_history.weekly_click if last_history is not None else 0,
            'affiliate_signup': last_history.weekly_signup if last_history is not None else 0,
            'affiliate_commission': last_history.weekly_commission if last_history is not None else 0.0,
            'rate': history.rate,
        })
    return results

def get_histories(mode, range = None):
    if mode == 'daily':
        initial_date = get_delta_date()
        histories = History.query.join(Affiliate).filter(History.created_at == initial_date).order_by(History.rate.desc()).all()
        results = []
        for history in histories:
            results.append({
                'id': history.affiliate_id,
                'name': history.affiliate.name,
                'click': history.daily_click,
                'signup': history.daily_signup,
                'commission': history.daily_commission,
                'affiliate_click': history.daily_click,
                'affiliate_signup': history.daily_signup,
                'affiliate_commission': history.daily_commission,
                'rate': history.rate,
            })
        return results
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
    issues = get_issues()

    return render_template(
        "home/dashboard.html",
        title = "Dashbaord",
        date = initial_date,
        histories = histories,
        issues = issues
    )


@home.route('/histories', methods = ['POST', 'GET'])
def api_histories():
    mode = request.json['mode']
    date_range = user = request.json['date_range']
    histories = get_histories(mode, date_range)

    return jsonify(status = True, data = histories)