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
        History.daily_click,
        History.daily_signup,
        History.daily_commission,
        History.rate,
        History.ga_click,
        History.ga_detail,
    ).filter(
        History.created_at >= start,
        History.created_at <= end
    ).join(History.affiliate).order_by('rate desc').all()

    pre_results = {}
    details = {}

    for history in histories:
        affiliate = history.name
        if pre_results.get(affiliate) is None:
            pre_results[affiliate] = {
                'id': history.id,
                'name': affiliate,
                'click': 0,
                'signup': 0,
                'commission': 0.0,
                'rate': 0.0,
                'ga_click': 0,
                'count': 0,
            }

        if counts.get(affiliate) is None:
            counts[affiliate] = 0
        
        pre_results[affiliate]['click'] += history.daily_click
        pre_results[affiliate]['signup'] += history.daily_signup
        pre_results[affiliate]['commission'] += history.daily_commission
        pre_results[affiliate]['rate'] += 0.0 if history.rate is None else history.rate
        pre_results[affiliate]['ga_click'] += 0 if history.ga_click is None else history.ga_click

        detail = history.ga_detail
        if detail is None:
            detail = "[]"
        detail = json.loads(detail)

        if details.get(affiliate) is None:
            details[affiliate] = {}
        for item in detail:
            if details[affiliate].get(item.get('label')) is None:
                details[affiliate][item.get('label')] = 0
            details[affiliate][item.get('label')] += int(item.get('clicks'))
        if history.rate > 0:
            pre_results[affiliate]['count'] += 1

    results = []
    for affiliate in pre_results:
        item = pre_results.get(affiliate)
        detail = details.get(affiliate)
        temp_detail = []
        for label in detail:
            temp_detail.append('{0}: {1}'.format(label, detail[label]))

        results.append({
            'id': item.get('id'),
            'name': item.get('name'),
            'click': item.get('click'),
            'signup': item.get('signup'),
            'commission': round(item.get('commission'), 2),
            'affiliate_click': item.get('click'),
            'affiliate_signup': item.get('signup'),
            'affiliate_commission': round(item.get('commission'), 2),
            'rate': round(item.get('rate') / item['count'], 2),
            'ga_click': item.get('ga_click'),
            'ga_detail': "\n".join(temp_detail),
        })
    return sorted(results, key = lambda k: k['rate'], reverse=True)

def get_histories(mode, range = None):
    if mode == 'daily':
        initial_date = get_delta_date()
        histories = History.query.join(Affiliate).filter(History.created_at == initial_date).order_by(History.rate.desc()).all()
        results = []
        for history in histories:
            if history.ga_detail is None:
                history.ga_detail = "[]"

            ga_details = json.loads(history.ga_detail)
            tooltip = []
            for item in ga_details:
                tooltip.append("{0}: {1}".format(item.get('label'), item.get('clicks')))

            results.append({
                'id': history.affiliate_id,
                'name': history.affiliate.name,
                'click': history.daily_click,
                'signup': history.daily_signup,
                'commission': round(history.daily_commission, 2),
                'affiliate_click': history.daily_click,
                'affiliate_signup': history.daily_signup,
                'affiliate_commission': round(history.daily_commission, 2),
                'rate': history.rate,
                'ga_click': history.ga_click,
                'ga_detail': "\n".join(tooltip)
            })
        return sorted(results, key = lambda k: k['rate'], reverse=True)
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


@home.route('/home/test')
def test():
    from ..spiders.ga import GoogleAnalyticsReport
    me = GoogleAnalyticsReport()
    response = me.run()
    return jsonify(status = True, data = response)

@home.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@home.errorhandler(404)
def page_not_found(e):
    logging.exception("Page not found.")
    return """
    Page not found: <pre>{}</pre>
    See logs for full track.
    """.format(e), 404