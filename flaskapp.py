# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, make_response# send_file, send_from_directory
import json, gc
from functools import wraps
from passlib.handlers.sha2_crypt import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  
from forex_python.converter import CurrencyRates, CurrencyCodes
import datetime
from sqlalchemy.ext.declarative import declarative_base
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import jinja2

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# from logs.views import log_app
# app.register_blueprint(log_app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

def datetimeformat(value, format='%Y/%m'):
    return value.strftime(format)

jinja2.filters.FILTERS['datetimeformat'] = datetimeformat

class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(10))
    message = db.Column(db.String(100))
    managed = db.Column(db.Boolean, unique = False, default = False)
    created_at = db.Column(db.Date)

    def __init__(self, provider, message, created_at, managed = False):
        self.provider = provider
        self.message = message
        self.managed = managed
        self.created_at = created_at

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Username %r>' % self.username


class Bet365(db.Model):
    __tablename__ = "bet365s"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    click = db.Column(db.Integer)
    nsignup = db.Column(db.Integer)
    ndepo = db.Column(db.Integer)
    valdepo = db.Column(db.Float)
    numdepo = db.Column(db.Integer)
    spotsturn = db.Column(db.Float)
    numsptbet = db.Column(db.Integer)
    acsptusr = db.Column(db.Integer)
    sptnetrev = db.Column(db.Float)
    casinonetrev = db.Column(db.Float)
    pokernetrev = db.Column(db.Float)
    bingonetrev = db.Column(db.Float)
    netrev = db.Column(db.Float)
    afspt = db.Column(db.Float)
    afcasino = db.Column(db.Float)
    afpoker = db.Column(db.Float)
    afbingo = db.Column(db.Float)
    commission = db.Column(db.Float)
    

    def __init__(self, dateto, click, nsignup, ndepo, valdepo, numdepo, spotsturn, numsptbet, acsptusr, sptnetrev, casinonetrev, pokernetrev, bingonetrev, netrev, afspt, afcasino, afpoker, afbingo, commission):
        self.dateto = dateto
        self.click = click
        self.nsignup = nsignup
        self.ndepo = ndepo
        self.valdepo = valdepo
        self.numdepo = numdepo
        self.spotsturn = spotsturn
        self.numsptbet = numsptbet
        self.acsptusr = acsptusr
        self.sptnetrev = sptnetrev
        self.casinonetrev = casinonetrev
        self.pokernetrev = pokernetrev
        self.bingonetrev = bingonetrev
        self.netrev = netrev
        self.afspt = afspt
        self.afcasino = afcasino
        self.afpoker = afpoker
        self.afbingo = afbingo
        self.commission = commission


class Bet365Other(db.Model):
    __tablename__ = "bet365others"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    click = db.Column(db.Integer)
    nsignup = db.Column(db.Integer)
    ndepo = db.Column(db.Integer)
    valdepo = db.Column(db.Float)
    numdepo = db.Column(db.Integer)
    spotsturn = db.Column(db.Float)
    numsptbet = db.Column(db.Integer)
    acsptusr = db.Column(db.Integer)
    sptnetrev = db.Column(db.Float)
    casinonetrev = db.Column(db.Float)
    pokernetrev = db.Column(db.Float)
    bingonetrev = db.Column(db.Float)
    netrev = db.Column(db.Float)
    afspt = db.Column(db.Float)
    afcasino = db.Column(db.Float)
    afpoker = db.Column(db.Float)
    afbingo = db.Column(db.Float)
    commission = db.Column(db.Float)
    
    def __init__(self, dateto, click, nsignup, ndepo, valdepo, numdepo, spotsturn, numsptbet, acsptusr, sptnetrev, casinonetrev, pokernetrev, bingonetrev, netrev, afspt, afcasino, afpoker, afbingo, commission):
        self.dateto = dateto
        self.click = click
        self.nsignup = nsignup
        self.ndepo = ndepo
        self.valdepo = valdepo
        self.numdepo = numdepo
        self.spotsturn = spotsturn
        self.numsptbet = numsptbet
        self.acsptusr = acsptusr
        self.sptnetrev = sptnetrev
        self.casinonetrev = casinonetrev
        self.pokernetrev = pokernetrev
        self.bingonetrev = bingonetrev
        self.netrev = netrev
        self.afspt = afspt
        self.afcasino = afcasino
        self.afpoker = afpoker
        self.afbingo = afbingo
        self.commission = commission


class Eight88(db.Model):
    __tablename__ = "eight88s"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    lead = db.Column(db.Integer)
    money_player = db.Column(db.Integer)
    balance = db.Column(db.Float)
    prebalance = db.Column(db.Float)
    imprwk = db.Column(db.Integer)
    cliwk = db.Column(db.Integer)
    regwk = db.Column(db.Integer)
    leadwk = db.Column(db.Integer)
    mpwk = db.Column(db.Integer)
    imprpre = db.Column(db.Integer)
    clipre = db.Column(db.Integer)
    regpre = db.Column(db.Integer)
    leadpre = db.Column(db.Integer)
    mppre = db.Column(db.Integer)
    imprto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    leadto = db.Column(db.Integer)
    mpto = db.Column(db.Integer)


    def __init__(self, impression, click, registration, lead, money_player, balance, prebalance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto, dateto):
        self.impression = impression
        self.click = click
        self.registration = registration
        self.lead = lead
        self.money_player = money_player
        self.balance = balance
        self.prebalance = prebalance
        self.imprwk = imprwk
        self.cliwk = cliwk
        self.regwk = regwk
        self.leadwk = leadwk
        self.mpwk = mpwk
        self.imprpre = imprpre
        self.clipre = clipre
        self.regpre = regpre
        self.leadpre = leadpre
        self.mppre = mppre
        self.imprto = imprto
        self.clito = clito
        self.regto = regto
        self.leadto = leadto
        self.mpto = mpto
        self.dateto = dateto


class Bet10(db.Model):
    __tablename__ = "bet10s"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    impreytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    impreto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.impreytd = impreytd
        self.cliytd = cliytd
        self.regytd = regytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.impreto = impreto
        self.clito = clito
        self.regto = regto
        self.ndto = ndto
        self.commito = commito
        self.dateto = dateto


class RealDeal(db.Model):
    __tablename__ = "realdeals"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    impreytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regiytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    impreto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regiytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.impreytd = impreytd
        self.cliytd = cliytd
        self.regiytd = regiytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.impreto = impreto
        self.clito = clito
        self.regto = regto
        self.ndto = ndto
        self.commito = commito
        self.dateto = dateto



class LadBroke(db.Model):
    __tablename__ = "ladbrokes"
    id = db.Column(db.Integer, primary_key=True)
    click = db.Column(db.Integer)
    signup = db.Column(db.Integer)
    commission = db.Column(db.Float)
    monthly_click = db.Column(db.Integer)
    monthly_signup = db.Column(db.Integer)
    monthly_commission = db.Column(db.Float)
    yearly_click = db.Column(db.Integer)
    yearly_signup = db.Column(db.Integer)
    yearly_commission = db.Column(db.Float)
    paid_signup = db.Column(db.Integer)
    created_at = db.Column(db.Date, unique = True)

    def __init__(self, click, signup, commmission, monthly_click, monthly_signup, monthly_commmission, yearly_click, yearly_signup, yearly_commmission, paid_signup, created_at):
        self.click = click
        self.signup = signup
        self.commission = commission
        self.monthly_click = monthly_click
        self.monthly_signup = monthly_signup
        self.monthly_commission = monthly_commission
        self.yearly_click = yearly_click
        self.yearly_signup = yearly_signup
        self.yearly_commission = yearly_commission
        self.paid_signup = paid_signup
        self.created_at = created_at


class BetFred(db.Model):
    __tablename__ = "betfreds"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    impreytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    impreto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.impreytd = impreytd
        self.cliytd = cliytd
        self.regytd = regytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.impreto = impreto
        self.clito = clito
        self.regto = regto
        self.ndto = ndto
        self.commito = commito
        self.dateto = dateto


class Victor(db.Model):
    __tablename__ = "victors"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    impreytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    impreto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito, dateto):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.impreytd = impreytd
        self.cliytd = cliytd
        self.regytd = regytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.impreto = impreto
        self.clito = clito
        self.regto = regto
        self.ndto = ndto
        self.commito = commito
        self.dateto = dateto


class Paddy(db.Model):
    __tablename__ = "paddyies"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    balance = db.Column(db.Float)
    views = db.Column(db.Integer)
    uniqueviews = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    uniqueclicks = db.Column(db.Float)
    signups = db.Column(db.Integer)
    depositingcustomers = db.Column(db.Float)
    activecustomers = db.Column(db.Float)
    newdepositingcustomers = db.Column(db.Float)
    newactivecustomers = db.Column(db.Float)
    firsttimedepositingcustomers = db.Column(db.Float)
    firsttimeactivecustomers = db.Column(db.Float)
    netrevenue = db.Column(db.Float)

    def __init__(self, dateto, views, uniqueviews, clicks, uniqueclicks, signups, depositingcustomers, activecustomers, newdepositingcustomers, newactivecustomers, firsttimedepositingcustomers, firsttimeactivecustomers, netrevenue):
        self.dateto = dateto
        self.balance = balance
        self.views = views
        self.uniqueviews = uniqueviews
        self.clicks = clicks
        self.uniqueclicks = uniqueclicks
        self.signups = signups
        self.depositingcustomers = depositingcustomers
        self.activecustomers = activecustomers
        self.newdepositingcustomers = newdepositingcustomers
        self.newactivecustomers = newactivecustomers
        self.firsttimedepositingcustomers = firsttimedepositingcustomers
        self.firsttimeactivecustomers = firsttimeactivecustomers
        self.netrevenue = netrevenue

class NetBet(db.Model):
    __tablename__ = "netbets"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, unique = True)
    click = db.Column(db.Integer)
    signup = db.Column(db.Integer)
    commission = db.Column(db.Float)
    monthly_click = db.Column(db.Integer)
    monthly_signup = db.Column(db.Integer)
    monthly_commission = db.Column(db.Float)
    yearly_click = db.Column(db.Integer)
    yearly_signup = db.Column(db.Integer)
    yearly_commission = db.Column(db.Float)
    paid_signup = db.Column(db.Integer)

    def __init__(self, click, signup, commission, monthly_click, monthly_signup, monthly_commission, yearly_click, yearly_signup, yearly_commission, paid_signup, created_at):
        self.click = click
        self.signup = signup
        self.commission = commission
        self.monthly_click = monthly_click
        self.monthly_signup = monthly_signup
        self.monthly_commission = monthly_commission
        self.yearly_click = yearly_click
        self.yearly_signup = yearly_signup
        self.yearly_commission = yearly_commission
        self.paid_signup = paid_signup
        self.created_at = created_at



class TitanBet(db.Model):
    __tablename__ = "titanbets"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    balance = db.Column(db.Float)
    tlr_amount = db.Column(db.Float)
    real_clicks = db.Column(db.Integer)
    casino_u_real_count = db.Column(db.Float)
    casino_d_rf_count  = db.Column(db.Float)
    casino_net_gaming = db.Column(db.Float)
    poker_u_real_count = db.Column(db.Float)
    poker_d_rf_count = db.Column(db.Float)
    poker_net_gaming = db.Column(db.Float)
    sport_u_real_count = db.Column(db.Float)
    sport_d_rf_count = db.Column(db.Float)

    def __init__(self, dateto, balance, tlr_amount, real_clicks, casino_u_real_count, casino_d_rf_count, casino_net_gaming, poker_u_real_count, poker_d_rf_count, poker_net_gaming, sport_u_real_count, sport_d_rf_count):
        self.dateto = dateto
        self.balance = balance
        self.tlr_amount = tlr_amount
        self.real_clicks = real_clicks
        self.casino_u_real_count = casino_u_real_count
        self.casino_d_rf_count = casino_d_rf_count
        self.casino_net_gaming = casino_net_gaming
        self.poker_u_real_count = poker_u_real_count
        self.poker_d_rf_count = poker_d_rf_count
        self.poker_net_gaming = poker_net_gaming
        self.sport_u_real_count = sport_u_real_count
        self.sport_d_rf_count = sport_d_rf_count


class Stan(db.Model):
    __tablename__ = "stans"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    impreytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    imprto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)

    def __init__(self, dateto, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, imprto, clito, regto, ndto, commito):
        self.dateto = dateto
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.impreytd = impreytd
        self.cliytd = cliytd
        self.regytd = regytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.imprto = imprto
        self.clito = clito
        self.regto = regto
        self.ndto = ndto
        self.commito = commito


class Coral(db.Model):
    __tablename__ = "corals"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    impreytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    impreto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)

    def __init__(self, dateto, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, impreto, clito, regto, ndto, commito):
        self.dateto = dateto
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.impreytd = impreytd
        self.cliytd = cliytd
        self.regytd = regytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.impreto = impreto
        self.clito = clito
        self.regto = regto
        self.ndto = ndto
        self.commito = commito


class William(db.Model):
    __tablename__ = "williams"
    id = db.Column(db.Integer, primary_key=True)
    click = db.Column(db.Integer)
    signup = db.Column(db.Integer)
    commission = db.Column(db.Float)
    monthly_click = db.Column(db.Integer)
    monthly_signup = db.Column(db.Integer)
    monthly_commission = db.Column(db.Float)
    yearly_click = db.Column(db.Integer)
    yearly_signup = db.Column(db.Integer)
    yearly_commission = db.Column(db.Float)
    paid_signup = db.Column(db.Integer)
    created_at = db.Column(db.Date, unique = True)

    def __init__(self, click, signup, commission, monthly_click, monthly_signup, monthly_commission, yearly_click, yearly_signup, yearly_commission, paid_signup, created_at):
        self.click = click
        self.signup = signup
        self.commission = commission
        self.monthly_click = monthly_click
        self.monthly_signup = monthly_signup
        self.monthly_commission = monthly_commission
        self.yearly_click = yearly_click
        self.yearly_signup = yearly_signup
        self.yearly_commission = yearly_commission
        self.paid_signup = paid_signup
        self.created_at = created_at


class SkyBet(db.Model):
    __tablename__ = "skybets"
    id = db.Column(db.Integer, primary_key=True)
    dateto = db.Column(db.Date, unique = True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    impreytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    imprto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regito = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)

    def __init__(self, dateto, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regytd, ndytd, commiytd, imprto, clito, regito, ndto, commito):
        self.dateto = dateto
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.impreytd = impreytd
        self.cliytd = cliytd
        self.regytd = regytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.imprto = imprto
        self.clito = clito
        self.regito = regito
        self.ndto = ndto
        self.commito = commito


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('login'))
    return wrap


@app.route('/logout/')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.')
    gc.collect()
    return redirect(url_for('login'))


#login form - redirect dashboard.
@app.route('/login/', methods = ['GET', 'POST'])
def login():
    error = ''
    try:
        username = request.form['username']
        if request.method == 'POST':
            data = db.session.query(User).filter_by(username = username).first()
            if not data:
                error = "Invalid credentials, try again."
            if sha256_crypt.verify(request.form['password'], data.password):
                session['logged_in'] = True
                session['username']  = request.form['username']

                flash('You are logged in!')
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid credentials, try again."
            gc.collect()
        return render_template('pages/user_sys/login.html', error = error)        
    except Exception as e:
        return render_template('pages/user_sys/login.html', error = error)


#register form
@app.route('/register/', methods = ['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = sha256_crypt.encrypt((str(request.form['password'])))
            
            user = db.session.query(User).filter_by(username = username).first()

            if not user:
                result = User(username, email, password)

                db.session.add(result)
                db.session.commit()

                flash('Thanks for registering!')
                gc.collect()
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('register'))
                
            else:
                flash('That username is already taken, please choose another.')

        return render_template('pages/user_sys/register.html')
    except Exception as e:
        return (str(e))


@app.route('/', methods = ['GET', 'POST'])
def landing():
    session.clear()
    flash("You need to login first.")
    return render_template('/pages/user_sys/login.html')


@app.route('/dashboard/', methods = ['GET', 'POST'])
@login_required
def dashboard():
    bet365 = db.session.query(Bet365).order_by(Bet365.id.desc()).first()
    eight88 = db.session.query(Eight88).order_by(Eight88.id.desc()).first()
    bet10 = db.session.query(Bet10).order_by(Bet10.id.desc()).first()
    realDeal = db.session.query(RealDeal).order_by(RealDeal.id.desc()).first()
    ladBroke = db.session.query(LadBroke).order_by(LadBroke.id.desc()).first()
    betFred = db.session.query(BetFred).order_by(BetFred.id.desc()).first()
    paddy = db.session.query(Paddy).order_by(Paddy.id.desc()).first()
    netBet = db.session.query(NetBet).order_by(NetBet.id.desc()).first()
    titanBet = db.session.query(TitanBet).order_by(TitanBet.id.desc()).first()
    stan = db.session.query(Stan).order_by(Stan.id.desc()).first()
    coral = db.session.query(Coral).order_by(Coral.id.desc()).first()
    william = db.session.query(William).order_by(William.id.desc()).first()
    skyBet = db.session.query(SkyBet).order_by(SkyBet.id.desc()).first()
    bet365other = db.session.query(Bet365Other).order_by(Bet365Other.id.desc()).first()
    victor = db.session.query(Victor).order_by(Victor.id.desc()).first()

    currency = CurrencyRates()
    sg_cur = CurrencyCodes()
    eur = float(currency.get_rate('EUR', 'USD'))
    gbp = float(currency.get_rate('GBP', 'USD'))

    sg_usd = sg_cur.get_symbol('USD')
    sg_eur = sg_cur.get_symbol('EUR')
    sg_gbp = sg_cur.get_symbol('GBP')

    valSg = [sg_usd, sg_eur, sg_gbp]

    currency = CurrencyRates()
    sg_cur = CurrencyCodes()
    eur = float(currency.get_rate('EUR', 'USD'))
    gbp = float(currency.get_rate('GBP', 'USD'))

    sg_usd = sg_cur.get_symbol('USD')
    sg_eur = sg_cur.get_symbol('EUR')
    sg_gbp = sg_cur.get_symbol('GBP')

    valSg = [sg_usd, sg_eur, sg_gbp]

    if request.method == 'GET':
        bet365Data = db.session.execute("""SELECT 
                    SUM(click)::int as click,
                    SUM(nSignup)::int as nsignup,
                    SUM(nDepo)::int as ndepo,
                    SUM(valDepo)::int as valdepo,
                    SUM(numDepo)::int as numdepo,
                    SUM(spotsTurn)::int as spotsturn,
                    SUM(numsptbet)::int as numsptbet,
                    SUM(acsptusr)::int as acsptusr,
                    SUM(sptnetrev)::int as sptnetrev,
                    SUM(casinonetrev)::int as casinonetrev,
                    SUM(pokernetrev)::int as pokernetrev,
                    SUM(bingonetrev)::int as bingonetrev,
                    SUM(netrev)::int as netrev,
                    SUM(afspt)::int as afspt,
                    SUM(afcasino)::int as afcasino,
                    SUM(afpoker)::int as afpoker,
                    SUM(afbingo)::int as afbingo,
                    SUM(commission)::int as commission,
                    EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
                FROM bet365s
                GROUP BY datefield
                ORDER By datefield DESC LIMIT 1;""").first()

        bet365otherData = db.session.execute("""SELECT 
                SUM(click)::int as click,
                SUM(nSignup)::int as nsignup,
                SUM(nDepo)::int as ndepo,
                SUM(valDepo)::int as valdepo,
                SUM(numDepo)::int as numdepo,
                SUM(spotsTurn)::int as spotsturn,
                SUM(numsptbet)::int as numsptbet,
                SUM(acsptusr)::int as acsptusr,
                SUM(sptnetrev)::int as sptnetrev,
                SUM(casinonetrev)::int as casinonetrev,
                SUM(pokernetrev)::int as pokernetrev,
                SUM(bingonetrev)::int as bingonetrev,
                SUM(netrev)::int as netrev,
                SUM(afspt)::int as afspt,
                SUM(afcasino)::int as afcasino,
                SUM(afpoker)::int as afpoker,
                SUM(afbingo)::int as afbingo,
                SUM(commission)::int as commission,
                EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
            FROM bet365others
            GROUP BY datefield
            ORDER By datefield DESC LIMIT 1;""").first()

        data = [bet365Data, eight88, bet10, realDeal, ladBroke, betFred, paddy, titanBet, stan, coral, eur, gbp, william, skyBet, netBet, bet365otherData, valSg, victor]
        issues = db.session.query(Log).filter(Log.managed==False).all()
        return render_template('home.html', data = data, issues = issues)

    if request.method == 'POST':
        val = request.json['val']
        state = request.json['state']
        if state == "1":
            dateStr = request.json['val']
            fromDate = dateStr.split("-")[0].strip(" ")
            toDate = dateStr.split("-")[1].strip(" ")

            startDate = datetime.datetime.strptime(fromDate, '%m/%d/%Y').date()
            endDate = datetime.datetime.strptime(toDate, '%m/%d/%Y').date()

            bet365 = db.session.execute("""SELECT 
                SUM(click)::int as click,
                SUM(nSignup)::int as nsignup,
                SUM(nDepo)::int as ndepo
            FROM bet365s
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()
            
            bet10 = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM bet10s
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            realDeal = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM realdeals
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            betFred = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM betfreds
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            stan = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM stans
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            coral = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM corals
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            skyBet = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regito)::int as registration,
                SUM(commito)::float as commission
            FROM skybets
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            bet365other = db.session.execute("""SELECT 
                SUM(click)::int as click,
                SUM(nSignup)::int as nsignup,
                SUM(nDepo)::int as ndepo
            FROM bet365others
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            victor = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM victors
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()
            

            tB3Odollar = (bet365other.ndepo or 0.0) * 100
            tB3dollar = (bet365.ndepo or 0.0) * 100

            tB10dollar = "%.2f" % round((bet10.commission or 0.0) * eur, 2) if bet10 is not None else "%.2f" % round(0.00)
            tRealdollar = "%.2f" % round((realDeal.commission or 0.0) * eur, 2) if realDeal is not None else "%.2f" % round(0.00)
            tSkydollar = "%.2f" % round((skyBet.commission or 0.0) * gbp, 2) if skyBet is not None else "%.2f" % round(0.00)
            tStandollar = stan.commission if stan is not None else "%.2f" % round(0.00)
            tBFdollar = "%.2f" % round((betFred.commission or 0.0) * gbp, 2) if betFred is not None else "%.2f" % round(0.00)
            tWildollar = "%.2f" % round((william.monthly_commission or 0.0) * eur, 2) if william is not None else "%.2f" % round(0.00)
            tLadollar = "%.2f" % round((ladBroke.monthly_commission or 0.0) * gbp, 2) if ladBroke is not None else "%.2f" % round(0.00)
            tPadollar = "%.2f" % round((paddy.balance or 0.0) * eur, 2) if paddy is not None else "%.2f" % round(0.00)
            tNetdollar = "%.2f" % round((netBet.monthly_commission or 0.0) * eur, 2) if netBet is not None else "%.2f" % round(0.00)
            tVidollar = "%.2f" % round((victor.commission or 0.0) * gbp, 2) if victor is not None else "%.2f" % round(0.00)

            jsonData = []
            jsonData.append({
                "tB3Oclick" : bet365other.click,
                "tB3Osignup" : bet365other.nsignup,
                "tB3Odepo" : bet365other.ndepo,
                "tB3Odollar" : tB3Odollar,

                "tB3click" : bet365.click,
                "tB3signup" : bet365.nsignup, 
                "tB3depo" : bet365.ndepo,
                "tB3dollar" : tB3dollar,

                "t8click" : eight88.clito,
                "t8register" : eight88.regto,
                "t8balance" : eight88.balance,
                "t8dollar" : eight88.balance,

                "tB10click" : bet10.click,
                "tB10register" : bet10.registration,
                "tB10commission" : bet10.commission,
                "tB10dollar" : tB10dollar,

                "tRealclick" : realDeal.click,
                "tRealregister" : realDeal.registration,
                "tRealcommission" : realDeal.commission,
                "tRealdollar" : tRealdollar,

                "tSkyclick" : skyBet.click,
                "tSkyregister" : skyBet.registration,
                "tSkycommission" : skyBet.commission,
                "tSkydollar": tSkydollar,

                "tWildollar" : tWildollar,
                
                "tLadollar" : tLadollar,
                
                "tPadollar" : tPadollar,
                
                "tNetdollar" : tNetdollar,
                
                "tTidollar" : titanBet.balance,

                "tStanclick" : stan.click,
                "tStanregister" : stan.registration,
                "tStancommission" : stan.commission,
                "tStandollar" : tStandollar,

                "tCoralclick" : coral.click,
                "tCoralregister" : coral.registration,
                "tCoralcommission" : coral.commission,
                "tCoraldollar" : coral.commission,

                "tBFclick" : betFred.click,
                "tBFregister" : betFred.registration,
                "tBFcommission" : betFred.commission,
                "tBFdollar" : tBFdollar,

                "tViclick" : victor.click,
                "tViregister" : victor.registration,
                "tVicommission" : victor.commission,
                "tVidollar" : tVidollar,

            })
            return jsonify(status = True, jsonData = jsonData)

        if state == "2":
            if val == "1":
                bet365Data = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
                    FROM bet365s
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365otherData = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
                    FROM bet365others
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365Date = bet365Data.datefield
                bet365OtherDate = bet365otherData.datefield
                tB3Odollar = bet365otherData.ndepo * 100
                tB3dollar = bet365Data.ndepo * 100
                tB10dollar = "%.2f" % round(bet10.commission * eur, 2)
                tRealdollar = "%.2f" % round(realDeal.commission * eur, 2)
                tSkydollar = "%.2f" % round(skyBet.commission * gbp, 2)
                tStandollar = stan.commission
                tBFdollar = "%.2f" % round(betFred.commission * gbp, 2)
                tWildollar = "%.2f" % round(william.monthly_commission * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.monthly_commission * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.monthly_commission * eur, 2)
                tVidollar = "%.2f" % round(victor.commission * eur, 2)

                jsonData = []
                jsonData.append({
                    "tB3Odate" : bet365OtherDate,
                    "tB3Oclick" : bet365otherData.click,
                    "tB3Osignup" : bet365otherData.nsignup,
                    "tB3Odepo" : bet365otherData.ndepo,
                    "tB3Odollar" : tB3Odollar,

                    "tB3date" : bet365Date,
                    "tB3click" : bet365Data.click,
                    "tB3signup" : bet365Data.nsignup, 
                    "tB3depo" : bet365Data.ndepo,
                    "tB3dollar" : tB3dollar,

                    "t8click" : eight88.click,
                    "t8register" : eight88.registration,
                    "t8balance" : eight88.balance,
                    "t8dollar" : eight88.balance,

                    "tB10click" : bet10.click,
                    "tB10register" : bet10.registration,
                    "tB10commission" : bet10.commission,
                    "tB10dollar" : tB10dollar,

                    "tRealclick" : realDeal.click,
                    "tRealregister" : realDeal.registration,
                    "tRealcommission" : realDeal.commission,
                    "tRealdollar" : tRealdollar,

                    "tSkyclick" : skyBet.click,
                    "tSkyregister" : skyBet.registration,
                    "tSkycommission" : skyBet.commission,
                    "tSkydollar": tSkydollar,

                    "tWildollar" : tWildollar,
                    
                    "tLadollar" : tLadollar,
                    
                    "tPadollar" : tPadollar,
                    
                    "tNetdollar" : tNetdollar,
                    
                    "tTidollar" : titanBet.balance,

                    "tStanclick" : stan.click,
                    "tStanregister" : stan.registration,
                    "tStancommission" : stan.commission,
                    "tStandollar" : tStandollar,

                    "tCoralclick" : coral.click,
                    "tCoralregister" : coral.registration,
                    "tCoralcommission" : coral.commission,
                    "tCoraldollar" : coral.commission,

                    "tBFclick" : betFred.click,
                    "tBFregister" : betFred.registration,
                    "tBFcommission" : betFred.commission,
                    "tBFdollar" : tBFdollar,

                    "tViclick" : victor.click,
                    "tViregister" : victor.registration,
                    "tVicommission" : victor.commission,
                    "tVidollar" : tVidollar,

                    # "total" : total
                })
                return jsonify(status = True, jsonData = jsonData)
            elif val == "2":
                bet365Data = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text AS datefield 
                    FROM bet365s
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365otherData = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text AS datefield 
                    FROM bet365others
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365Date = bet365Data.datefield
                bet365OtherDate = bet365otherData.datefield
                tB3Odollar = bet365otherData.ndepo * 100
                tB3dollar = bet365Data.ndepo * 100
                tB10dollar = "%.2f" % round(bet10.commiytd * eur, 2)
                tRealdollar = "%.2f" % round(realDeal.commiytd * eur, 2)
                tSkydollar = "%.2f" % round(skyBet.commiytd * gbp, 2)
                tStandollar = stan.commiytd
                tBFdollar = "%.2f" % round(betFred.commiytd * gbp, 2)
                tWildollar = "%.2f" % round(william.monthly_commission * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.monthly_commission * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.monthly_commission * eur, 2)
                tVidollar = "%.2f" % round(victor.commiytd * eur, 2)


                jsonData = []
                jsonData.append({
                    "tB3Odate" : bet365OtherDate,
                    "tB3Oclick" : bet365otherData.click,
                    "tB3Osignup" : bet365otherData.nsignup,
                    "tB3Odepo" : bet365otherData.ndepo,
                    "tB3Odollar" : tB3Odollar,

                    "tB3date" : bet365Date,
                    "tB3click" : bet365Data.click,
                    "tB3signup" : bet365Data.nsignup, 
                    "tB3depo" : bet365Data.ndepo,
                    "tB3dollar" : tB3dollar,

                    "t8click" : eight88.click,
                    "t8register" : eight88.registration,
                    "t8balance" : eight88.balance,
                    "t8dollar" : eight88.balance,

                    "tB10click" : bet10.cliytd,
                    "tB10register" : bet10.regytd,
                    "tB10commission" : bet10.commiytd,
                    "tB10dollar" : tB10dollar,

                    "tRealclick" : realDeal.cliytd,
                    "tRealregister" : realDeal.regiytd,
                    "tRealcommission" : realDeal.commiytd,
                    "tRealdollar" : tRealdollar,

                    "tSkyclick" : skyBet.cliytd,
                    "tSkyregister" : skyBet.regytd,
                    "tSkycommission" : skyBet.commiytd,
                    "tSkydollar": tSkydollar,

                    "tWildollar" : tWildollar,
                    
                    "tLadollar" : tLadollar,
                    
                    "tPadollar" : tPadollar,
                    
                    "tNetdollar" : tNetdollar,
                    
                    "tTidollar" : titanBet.balance,

                    "tStanclick" : stan.cliytd,
                    "tStanregister" : stan.regytd,
                    "tStancommission" : stan.commiytd,
                    "tStandollar" : tStandollar,

                    "tCoralclick" : coral.cliytd,
                    "tCoralregister" : coral.regytd,
                    "tCoralcommission" : coral.commiytd,
                    "tCoraldollar" : coral.commiytd,

                    "tBFclick" : betFred.cliytd,
                    "tBFregister" : betFred.regytd,
                    "tBFcommission" : betFred.commiytd,
                    "tBFdollar" : tBFdollar,

                    "tViclick" : victor.cliytd,
                    "tViregister" : victor.regytd,
                    "tVicommission" : victor.commiytd,
                    "tVidollar" : tVidollar,

                    # "total" : total
                })
                return jsonify(status = True, jsonData = jsonData)



@app.route('/summary/', methods = ['GET', 'POST'])
def summary():
    bet365 = db.session.query(Bet365).order_by(Bet365.id.desc()).first()
    eight88 = db.session.query(Eight88).order_by(Eight88.id.desc()).first()
    bet10 = db.session.query(Bet10).order_by(Bet10.id.desc()).first()
    realDeal = db.session.query(RealDeal).order_by(RealDeal.id.desc()).first()
    ladBroke = db.session.query(LadBroke).order_by(LadBroke.id.desc()).first()
    betFred = db.session.query(BetFred).order_by(BetFred.id.desc()).first()
    paddy = db.session.query(Paddy).order_by(Paddy.id.desc()).first()
    netBet = db.session.query(NetBet).order_by(NetBet.id.desc()).first()
    titanBet = db.session.query(TitanBet).order_by(TitanBet.id.desc()).first()
    stan = db.session.query(Stan).order_by(Stan.id.desc()).first()
    coral = db.session.query(Coral).order_by(Coral.id.desc()).first()
    william = db.session.query(William).order_by(William.id.desc()).first()
    skyBet = db.session.query(SkyBet).order_by(SkyBet.id.desc()).first()
    bet365other = db.session.query(Bet365Other).order_by(Bet365Other.id.desc()).first()
    victor = db.session.query(Victor).order_by(Victor.id.desc()).first()

    currency = CurrencyRates()
    sg_cur = CurrencyCodes()
    eur = float(currency.get_rate('EUR', 'USD'))
    gbp = float(currency.get_rate('GBP', 'USD'))

    sg_usd = sg_cur.get_symbol('USD')
    sg_eur = sg_cur.get_symbol('EUR')
    sg_gbp = sg_cur.get_symbol('GBP')

    valSg = [sg_usd, sg_eur, sg_gbp]

    if request.method == 'GET':
        bet365Data = db.session.execute("""SELECT 
                    SUM(click)::int as click,
                    SUM(nSignup)::int as nsignup,
                    SUM(nDepo)::int as ndepo,
                    SUM(valDepo)::int as valdepo,
                    SUM(numDepo)::int as numdepo,
                    SUM(spotsTurn)::int as spotsturn,
                    SUM(numsptbet)::int as numsptbet,
                    SUM(acsptusr)::int as acsptusr,
                    SUM(sptnetrev)::int as sptnetrev,
                    SUM(casinonetrev)::int as casinonetrev,
                    SUM(pokernetrev)::int as pokernetrev,
                    SUM(bingonetrev)::int as bingonetrev,
                    SUM(netrev)::int as netrev,
                    SUM(afspt)::int as afspt,
                    SUM(afcasino)::int as afcasino,
                    SUM(afpoker)::int as afpoker,
                    SUM(afbingo)::int as afbingo,
                    SUM(commission)::int as commission,
                    EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
                FROM bet365s
                GROUP BY datefield
                ORDER By datefield DESC LIMIT 1;""").first()

        bet365otherData = db.session.execute("""SELECT 
                SUM(click)::int as click,
                SUM(nSignup)::int as nsignup,
                SUM(nDepo)::int as ndepo,
                SUM(valDepo)::int as valdepo,
                SUM(numDepo)::int as numdepo,
                SUM(spotsTurn)::int as spotsturn,
                SUM(numsptbet)::int as numsptbet,
                SUM(acsptusr)::int as acsptusr,
                SUM(sptnetrev)::int as sptnetrev,
                SUM(casinonetrev)::int as casinonetrev,
                SUM(pokernetrev)::int as pokernetrev,
                SUM(bingonetrev)::int as bingonetrev,
                SUM(netrev)::int as netrev,
                SUM(afspt)::int as afspt,
                SUM(afcasino)::int as afcasino,
                SUM(afpoker)::int as afpoker,
                SUM(afbingo)::int as afbingo,
                SUM(commission)::int as commission,
                EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
            FROM bet365others
            GROUP BY datefield
            ORDER By datefield DESC LIMIT 1;""").first()
       
        data = [bet365Data, eight88, bet10, realDeal, ladBroke, betFred, paddy, titanBet, stan, coral, eur, gbp, william, skyBet, netBet, bet365otherData, valSg, victor]

        issues = db.session.query(Log).filter(Log.managed==False).all()
        return render_template('pages/summary.html', data = data, issues = issues)

    if request.method == 'POST':
        val = request.json['val']
        state = request.json['state']
        if state == "1":
            dateStr = request.json['val']
            fromDate = dateStr.split("-")[0].strip(" ")
            toDate = dateStr.split("-")[1].strip(" ")

            startDate = datetime.datetime.strptime(fromDate, '%m/%d/%Y').date()
            endDate = datetime.datetime.strptime(toDate, '%m/%d/%Y').date()

            bet365 = db.session.execute("""SELECT 
                SUM(click)::int as click,
                SUM(nSignup)::int as nsignup,
                SUM(nDepo)::int as ndepo
            FROM bet365s
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()
            
            bet10 = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM bet10s
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            realDeal = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM realdeals
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            betFred = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM betfreds
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            stan = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM stans
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            coral = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM corals
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            skyBet = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regito)::int as registration,
                SUM(commito)::float as commission
            FROM skybets
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            bet365other = db.session.execute("""SELECT 
                SUM(click)::int as click,
                SUM(nSignup)::int as nsignup,
                SUM(nDepo)::int as ndepo
            FROM bet365others
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()

            victor = db.session.execute("""SELECT 
                SUM(clito)::int as click,
                SUM(regto)::int as registration,
                SUM(commito)::float as commission
            FROM victors
            WHERE dateto >='%s' AND dateto <= '%s'""" % (startDate, toDate)).first()
            
            tB3Odollar = (bet365other.ndepo or 0.0) * 100
            tB3dollar = (bet365.ndepo or 0.0) * 100
            tB10dollar = "%.2f" % round((bet10.commission or 0.0) * eur, 2) if bet10 is not None else 0.0
            tRealdollar = "%.2f" % round((realDeal.commission or 0.0) * eur, 2) if realDeal is not None else 0.0
            tSkydollar = "%.2f" % round((skyBet.commission or 0.0) * gbp, 2) if skyBet is not None else 0.0
            tStandollar = stan.commission if stan is not None else 0.0
            tBFdollar = "%.2f" % round((betFred.commission or 0.0) * gbp, 2) if betFred is not None else 0.0
            tWildollar = "%.2f" % round((william.monthly_commission or 0.0) * eur, 2) if william is not None else 0.0
            tLadollar = "%.2f" % round((ladBroke.monthly_commission or 0.0) * gbp, 2) if ladBroke is not None else 0.0
            tPadollar = "%.2f" % round((paddy.balance or 0.0) * eur, 2) if paddy is not None else 0.0
            tNetdollar = "%.2f" % round((netBet.monthly_commission or 0.0) * eur, 2) if netBet is not None else 0.0
            tVidollar = "%.2f" % round((victor.commission or 0.0) * gbp, 2) if victor is not None else 0.0

            jsonData = []
            jsonData.append({
                "tB3Oclick" : bet365other.click,
                "tB3Osignup" : bet365other.nsignup,
                "tB3Odepo" : bet365other.ndepo,
                "tB3Odollar" : tB3Odollar,

                "tB3click" : bet365.click,
                "tB3signup" : bet365.nsignup, 
                "tB3depo" : bet365.ndepo,
                "tB3dollar" : tB3dollar,

                "t8click" : eight88.clito,
                "t8register" : eight88.regto,
                "t8balance" : eight88.balance,
                "t8dollar" : eight88.balance,

                "tB10click" : bet10.click,
                "tB10register" : bet10.registration,
                "tB10commission" : bet10.commission,
                "tB10dollar" : tB10dollar,

                "tRealclick" : realDeal.click,
                "tRealregister" : realDeal.registration,
                "tRealcommission" : realDeal.commission,
                "tRealdollar" : tRealdollar,

                "tSkyclick" : skyBet.click,
                "tSkyregister" : skyBet.registration,
                "tSkycommission" : skyBet.commission,
                "tSkydollar": tSkydollar,

                "tWildollar" : tWildollar,
                
                "tLadollar" : tLadollar,
                
                "tPadollar" : tPadollar,
                
                "tNetdollar" : tNetdollar,
                
                "tTidollar" : titanBet.balance,

                "tStanclick" : stan.click,
                "tStanregister" : stan.registration,
                "tStancommission" : stan.commission,
                "tStandollar" : tStandollar,

                "tCoralclick" : coral.click,
                "tCoralregister" : coral.registration,
                "tCoralcommission" : coral.commission,
                "tCoraldollar" : coral.commission,

                "tBFclick" : betFred.click,
                "tBFregister" : betFred.registration,
                "tBFcommission" : betFred.commission,
                "tBFdollar" : tBFdollar,

                "tViclick" : victor.click,
                "tViregister" : victor.registration,
                "tVicommission" : victor.commission,
                "tVidollar" : tVidollar,

            })
            return jsonify(status = True, jsonData = jsonData)

        if state == "2":
            if val == "1":
                bet365Data = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
                    FROM bet365s
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365otherData = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
                    FROM bet365others
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365Date = bet365Data.datefield
                bet365OtherDate = bet365otherData.datefield
                tB3Odollar = bet365otherData.ndepo * 100
                tB3dollar = bet365Data.ndepo * 100
                tB10dollar = "%.2f" % round(bet10.commission * eur, 2)
                tRealdollar = "%.2f" % round(realDeal.commission * eur, 2)
                tSkydollar = "%.2f" % round(skyBet.commission * gbp, 2)
                tStandollar = stan.commission
                tBFdollar = "%.2f" % round(betFred.commission * gbp, 2)
                tWildollar = "%.2f" % round(william.monthly_commission * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.monthly_commission * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.monthly_commission * eur, 2)
                tVidollar = "%.2f" % round(victor.commission * gbp, 2)

                jsonData = []
                jsonData.append({
                    "tB3Odate" : bet365OtherDate,
                    "tB3Oclick" : bet365otherData.click,
                    "tB3Osignup" : bet365otherData.nsignup,
                    "tB3Odepo" : bet365otherData.ndepo,
                    "tB3Odollar" : tB3Odollar,

                    "tB3date" : bet365Date,
                    "tB3click" : bet365Data.click,
                    "tB3signup" : bet365Data.nsignup, 
                    "tB3depo" : bet365Data.ndepo,
                    "tB3dollar" : tB3dollar,

                    "t8click" : eight88.click,
                    "t8register" : eight88.registration,
                    "t8balance" : eight88.balance,
                    "t8dollar" : eight88.balance,

                    "tB10click" : bet10.click,
                    "tB10register" : bet10.registration,
                    "tB10commission" : bet10.commission,
                    "tB10dollar" : tB10dollar,

                    "tRealclick" : realDeal.click,
                    "tRealregister" : realDeal.registration,
                    "tRealcommission" : realDeal.commission,
                    "tRealdollar" : tRealdollar,

                    "tSkyclick" : skyBet.click,
                    "tSkyregister" : skyBet.registration,
                    "tSkycommission" : skyBet.commission,
                    "tSkydollar": tSkydollar,

                    "tWildollar" : tWildollar,
                    
                    "tLadollar" : tLadollar,
                    
                    "tPadollar" : tPadollar,
                    
                    "tNetdollar" : tNetdollar,
                    
                    "tTidollar" : titanBet.balance,

                    "tStanclick" : stan.click,
                    "tStanregister" : stan.registration,
                    "tStancommission" : stan.commission,
                    "tStandollar" : tStandollar,

                    "tCoralclick" : coral.click,
                    "tCoralregister" : coral.registration,
                    "tCoralcommission" : coral.commission,
                    "tCoraldollar" : coral.commission,

                    "tBFclick" : betFred.click,
                    "tBFregister" : betFred.registration,
                    "tBFcommission" : betFred.commission,
                    "tBFdollar" : tBFdollar,

                    "tViclick" : victor.click,
                    "tViregister" : victor.registration,
                    "tVicommission" : victor.commission,
                    "tVidollar" : tVidollar,

                    # "total" : total
                })
                return jsonify(status = True, jsonData = jsonData)
            elif val == "2":
                bet365Data = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text AS datefield 
                    FROM bet365s
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365otherData = db.session.execute("""SELECT 
                        SUM(click)::int as click,
                        SUM(nSignup)::int as nsignup,
                        SUM(nDepo)::int as ndepo,
                        SUM(valDepo)::int as valdepo,
                        SUM(numDepo)::int as numdepo,
                        SUM(spotsTurn)::int as spotsturn,
                        SUM(numsptbet)::int as numsptbet,
                        SUM(acsptusr)::int as acsptusr,
                        SUM(sptnetrev)::int as sptnetrev,
                        SUM(casinonetrev)::int as casinonetrev,
                        SUM(pokernetrev)::int as pokernetrev,
                        SUM(bingonetrev)::int as bingonetrev,
                        SUM(netrev)::int as netrev,
                        SUM(afspt)::int as afspt,
                        SUM(afcasino)::int as afcasino,
                        SUM(afpoker)::int as afpoker,
                        SUM(afbingo)::int as afbingo,
                        SUM(commission)::int as commission,
                        EXTRACT(YEAR FROM dateto)::text AS datefield 
                    FROM bet365others
                    GROUP BY datefield
                    ORDER By datefield DESC LIMIT 1;""").first()

                bet365Date = bet365Data.datefield
                bet365OtherDate = bet365otherData.datefield
                tB3Odollar = bet365otherData.ndepo * 100
                tB3dollar = bet365Data.ndepo * 100
                tB10dollar = "%.2f" % round(bet10.commiytd * eur, 2)
                tRealdollar = "%.2f" % round(realDeal.commiytd * eur, 2)
                tSkydollar = "%.2f" % round(skyBet.commiytd * gbp, 2)
                tStandollar = stan.commiytd
                tBFdollar = "%.2f" % round(betFred.commiytd * gbp, 2)
                tWildollar = "%.2f" % round(william.monthly_commission * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.monthly_commission * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.monthly_commission * eur, 2)
                tVidollar = "%.2f" % round(victor.commiytd * gbp, 2)

                # totalVal = float(tB3Odollar) + float(tB3dollar) + float(tB10dollar) + float(tRealdollar) + float(tSkydollar) + float(tStandollar) + float(coral.commiytd) + float(tBFdollar)
                # total = "%.2f" % round(totalVal, 2)

                jsonData = []
                jsonData.append({
                    "tB3Odate" : bet365OtherDate,
                    "tB3Oclick" : bet365otherData.click,
                    "tB3Osignup" : bet365otherData.nsignup,
                    "tB3Odepo" : bet365otherData.ndepo,
                    "tB3Odollar" : tB3Odollar,

                    "tB3date" : bet365Date,
                    "tB3click" : bet365Data.click,
                    "tB3signup" : bet365Data.nsignup, 
                    "tB3depo" : bet365Data.ndepo,
                    "tB3dollar" : tB3dollar,

                    "t8click" : eight88.click,
                    "t8register" : eight88.registration,
                    "t8balance" : eight88.balance,
                    "t8dollar" : eight88.balance,

                    "tB10click" : bet10.cliytd,
                    "tB10register" : bet10.regytd,
                    "tB10commission" : bet10.commiytd,
                    "tB10dollar" : tB10dollar,

                    "tRealclick" : realDeal.cliytd,
                    "tRealregister" : realDeal.regiytd,
                    "tRealcommission" : realDeal.commiytd,
                    "tRealdollar" : tRealdollar,

                    "tSkyclick" : skyBet.cliytd,
                    "tSkyregister" : skyBet.regytd,
                    "tSkycommission" : skyBet.commiytd,
                    "tSkydollar": tSkydollar,

                    "tWildollar" : tWildollar,
                    
                    "tLadollar" : tLadollar,
                    
                    "tPadollar" : tPadollar,
                    
                    "tNetdollar" : tNetdollar,
                    
                    "tTidollar" : titanBet.balance,

                    "tStanclick" : stan.cliytd,
                    "tStanregister" : stan.regytd,
                    "tStancommission" : stan.commiytd,
                    "tStandollar" : tStandollar,

                    "tCoralclick" : coral.cliytd,
                    "tCoralregister" : coral.regytd,
                    "tCoralcommission" : coral.commiytd,
                    "tCoraldollar" : coral.commiytd,

                    "tBFclick" : betFred.cliytd,
                    "tBFregister" : betFred.regytd,
                    "tBFcommission" : betFred.commiytd,
                    "tBFdollar" : tBFdollar,

                    "tViclick" : victor.cliytd,
                    "tViregister" : victor.regytd,
                    "tVicommission" : victor.commiytd,
                    "tVidollar" : tVidollar,

                    # "total" : total
                })
                return jsonify(status = True, jsonData = jsonData)



@app.route('/bet365/', methods = ['GET', 'POST'])
def bet365():
    data = {}
    if request.method == 'GET':
        now = datetime.datetime.now()
        today = now.date()
        data = db.session.query(Bet365).filter(Bet365.dateto == today)
        issues = db.session.query(Log).filter(Log.managed==False).all()
        return render_template('pages/bet365.html', data = data, issues = issues)

    elif request.method == 'POST': 
        period = request.json['period']
        optVal = request.json['optVal']
        
        fromDate = datetime.datetime.strptime(period.split('-')[0].strip(), '%m/%d/%Y').date()
        toDate = datetime.datetime.strptime(period.split('-')[1].strip(), '%m/%d/%Y').date()
        
        jsonData = []
        if (optVal == '0') or (optVal == '1'):
            data = db.session.execute("""SELECT 
                *,
                EXTRACT(YEAR FROM dateto)::text || '-' ||EXTRACT(MONTH FROM dateto)::text || '-' || EXTRACT(DAY FROM dateto)::text AS datefield 
            FROM bet365s
            WHERE dateto >= '%s' AND dateto <= '%s'
            ORDER By datefield;""" % (fromDate, toDate))
            
            for perDay in data:
                jsonData.append({
                    "dateto" : perDay.datefield,
                    "click" : perDay.click,
                    "nSignup" : perDay.nsignup,
                    "nDepo" : perDay.ndepo,
                    "valDepo" : perDay.valdepo,
                    "numDepo" : perDay.numdepo,
                    "spotsTurn" : perDay.spotsturn,
                    "numSptBet" : perDay.numsptbet,
                    "acSptUsr" : perDay.acsptusr,
                    "sptNetRev" : perDay.sptnetrev,
                    "casinoNetRev" : perDay.casinonetrev,
                    "pokerNetRev" : perDay.pokernetrev,
                    "bingoNetRev" : perDay.bingonetrev,
                    "netRev" : perDay.netrev,
                    "afSpt" : perDay.afspt,
                    "afCasino" : perDay.afcasino,
                    "afPoker" : perDay.afpoker,
                    "afBingo" : perDay.afbingo,
                    "commission" : perDay.commission
                    })
            return jsonify(jsonData = jsonData)

        elif optVal == '2':
            data = db.session.execute("""SELECT 
                SUM(click) as click,
                SUM(nSignup) as nsignup,
                SUM(nDepo) as ndepo,
                SUM(valDepo) as valdepo,
                SUM(numDepo) as numdepo,
                SUM(spotsTurn) as spotsturn,
                SUM(numsptbet) as numsptbet,
                SUM(acsptusr) as acsptusr,
                SUM(sptnetrev) as sptnetrev,
                SUM(casinonetrev) as casinonetrev,
                SUM(pokernetrev) as pokernetrev,
                SUM(bingonetrev) as bingonetrev,
                SUM(netrev) as netrev,
                SUM(afspt) as afspt,
                SUM(afcasino) as afcasino,
                SUM(afpoker) as afpoker,
                SUM(afbingo) as afbingo,
                SUM(commission) as commission,
                EXTRACT(YEAR FROM dateto)::text || '/' ||EXTRACT(MONTH FROM dateto)::text || '(' || EXTRACT(WEEK FROM dateto)::text || 'wk.' || ')' AS datefield 
            FROM bet365s
            WHERE dateto >= '%s' AND dateto <= '%s'
            GROUP BY datefield
            ORDER By datefield;""" % (fromDate, toDate))

        elif optVal == '3':            
            data = db.session.execute("""SELECT 
                SUM(click) as click,
                SUM(nSignup) as nsignup,
                SUM(nDepo) as ndepo,
                SUM(valDepo) as valdepo,
                SUM(numDepo) as numdepo,
                SUM(spotsTurn) as spotsturn,
                SUM(numsptbet) as numsptbet,
                SUM(acsptusr) as acsptusr,
                SUM(sptnetrev) as sptnetrev,
                SUM(casinonetrev) as casinonetrev,
                SUM(pokernetrev) as pokernetrev,
                SUM(bingonetrev) as bingonetrev,
                SUM(netrev) as netrev,
                SUM(afspt) as afspt,
                SUM(afcasino) as afcasino,
                SUM(afpoker) as afpoker,
                SUM(afbingo) as afbingo,
                SUM(commission) as commission,
                EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
            FROM bet365s
            WHERE dateto >= '%s' AND dateto <= '%s'
            GROUP BY datefield
            ORDER By datefield;""" % (fromDate, toDate))
                    
        for perDay in data:
            jsonData.append({
                "dateto" : perDay.datefield,
                "click" : perDay.click,
                "nSignup" : perDay.nsignup,
                "nDepo" : perDay.ndepo,
                "valDepo" : perDay.valdepo,
                "numDepo" : perDay.numdepo,
                "spotsTurn" : perDay.spotsturn,
                "numSptBet" : perDay.numsptbet,
                "acSptUsr" : perDay.acsptusr,
                "sptNetRev" : perDay.sptnetrev,
                "casinoNetRev" : perDay.casinonetrev,
                "pokerNetRev" : perDay.pokernetrev,
                "bingoNetRev" : perDay.bingonetrev,
                "netRev" : perDay.netrev,
                "afSpt" : perDay.afspt,
                "afCasino" : perDay.afcasino,
                "afPoker" : perDay.afpoker,
                "afBingo" : perDay.afbingo,
                "commission" : perDay.commission
            })
        return jsonify(jsonData = jsonData)


@app.route('/bet365other/', methods = ['GET', 'POST'])
def bet365other():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        now = datetime.datetime.now()
        today = now.date()
        data = db.session.query(Bet365Other).filter(Bet365Other.dateto == today)
        return render_template('pages/bet365other.html', data = data, issues = issues)

    elif request.method == 'POST': 
        period = request.json['period']
        optVal = request.json['optVal']
        
        fromDate = datetime.datetime.strptime(period.split('-')[0].strip(), '%m/%d/%Y').date()
        toDate = datetime.datetime.strptime(period.split('-')[1].strip(), '%m/%d/%Y').date()
        
        jsonData = []
        if (optVal == '0') or (optVal == '1'):
            data = db.session.execute("""SELECT 
                *,
                EXTRACT(YEAR FROM dateto)::text || '-' ||EXTRACT(MONTH FROM dateto)::text || '-' || EXTRACT(DAY FROM dateto)::text AS datefield 
            FROM bet365others
            WHERE dateto >= '%s' AND dateto <= '%s'
            ORDER By datefield;""" % (fromDate, toDate))
            
            for perDay in data:
                jsonData.append({
                    "dateto" : perDay.datefield,
                    "click" : perDay.click,
                    "nSignup" : perDay.nsignup,
                    "nDepo" : perDay.ndepo,
                    "valDepo" : perDay.valdepo,
                    "numDepo" : perDay.numdepo,
                    "spotsTurn" : perDay.spotsturn,
                    "numSptBet" : perDay.numsptbet,
                    "acSptUsr" : perDay.acsptusr,
                    "sptNetRev" : perDay.sptnetrev,
                    "casinoNetRev" : perDay.casinonetrev,
                    "pokerNetRev" : perDay.pokernetrev,
                    "bingoNetRev" : perDay.bingonetrev,
                    "netRev" : perDay.netrev,
                    "afSpt" : perDay.afspt,
                    "afCasino" : perDay.afcasino,
                    "afPoker" : perDay.afpoker,
                    "afBingo" : perDay.afbingo,
                    "commission" : perDay.commission
                    })
            return jsonify(jsonData = jsonData)

        elif optVal == '2':
            data = db.session.execute("""SELECT 
                SUM(click) as click,
                SUM(nSignup) as nsignup,
                SUM(nDepo) as ndepo,
                SUM(valDepo) as valdepo,
                SUM(numDepo) as numdepo,
                SUM(spotsTurn) as spotsturn,
                SUM(numsptbet) as numsptbet,
                SUM(acsptusr) as acsptusr,
                SUM(sptnetrev) as sptnetrev,
                SUM(casinonetrev) as casinonetrev,
                SUM(pokernetrev) as pokernetrev,
                SUM(bingonetrev) as bingonetrev,
                SUM(netrev) as netrev,
                SUM(afspt) as afspt,
                SUM(afcasino) as afcasino,
                SUM(afpoker) as afpoker,
                SUM(afbingo) as afbingo,
                SUM(commission) as commission,
                EXTRACT(YEAR FROM dateto)::text || '/' ||EXTRACT(MONTH FROM dateto)::text || '(' || EXTRACT(WEEK FROM dateto)::text || 'wk.' || ')' AS datefield 
            FROM bet365others
            WHERE dateto >= '%s' AND dateto <= '%s'
            GROUP BY datefield
            ORDER By datefield;""" % (fromDate, toDate))

        elif optVal == '3':            
            data = db.session.execute("""SELECT 
                SUM(click) as click,
                SUM(nSignup) as nsignup,
                SUM(nDepo) as ndepo,
                SUM(valDepo) as valdepo,
                SUM(numDepo) as numdepo,
                SUM(spotsTurn) as spotsturn,
                SUM(numsptbet) as numsptbet,
                SUM(acsptusr) as acsptusr,
                SUM(sptnetrev) as sptnetrev,
                SUM(casinonetrev) as casinonetrev,
                SUM(pokernetrev) as pokernetrev,
                SUM(bingonetrev) as bingonetrev,
                SUM(netrev) as netrev,
                SUM(afspt) as afspt,
                SUM(afcasino) as afcasino,
                SUM(afpoker) as afpoker,
                SUM(afbingo) as afbingo,
                SUM(commission) as commission,
                EXTRACT(YEAR FROM dateto)::text || '/' || EXTRACT(MONTH FROM dateto)::text AS datefield 
            FROM bet365others
            WHERE dateto >= '%s' AND dateto <= '%s'
            GROUP BY datefield
            ORDER By datefield;""" % (fromDate, toDate))
                    
        for perDay in data:
            jsonData.append({
                "dateto" : perDay.datefield,
                "click" : perDay.click,
                "nSignup" : perDay.nsignup,
                "nDepo" : perDay.ndepo,
                "valDepo" : perDay.valdepo,
                "numDepo" : perDay.numdepo,
                "spotsTurn" : perDay.spotsturn,
                "numSptBet" : perDay.numsptbet,
                "acSptUsr" : perDay.acsptusr,
                "sptNetRev" : perDay.sptnetrev,
                "casinoNetRev" : perDay.casinonetrev,
                "pokerNetRev" : perDay.pokernetrev,
                "bingoNetRev" : perDay.bingonetrev,
                "netRev" : perDay.netrev,
                "afSpt" : perDay.afspt,
                "afCasino" : perDay.afcasino,
                "afPoker" : perDay.afpoker,
                "afBingo" : perDay.afbingo,
                "commission" : perDay.commission
            })
        return jsonify(jsonData = jsonData)


@app.route('/eight88/', methods = ['GET', 'POST'])
def eight88():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        data = db.session.query(Eight88).order_by(Eight88.id.desc()).first()
        return render_template('pages/eight88.html', data = data, issues = issues)
    if request.method == 'POST':
        data = db.session.query(Eight88).order_by(Eight88.id.desc()).first()
        jsonData = []
        jsonData.append({
            "impression" : data.impression,
            "click" : data.click,
            "registration" : data.registration,
            "lead" : data.lead,
            "money_player" : data.money_player,
            "balance" : data.balance,
            "prebalance" : data.prebalance,
            "imprwk" : data.imprwk,
            "cliwk" : data.cliwk,
            "regwk" : data.regwk,
            "leadwk" : data.leadwk,
            "mpwk" : data.mpwk,
            "imprpre" : data.imprpre,
            "clipre" : data.clipre,
            "regpre" : data.regpre,
            "leadpre" : data.leadpre,
            "mppre" : data.mppre,
            "imprto" : data.imprto,
            "clito" : data.clito,
            "regto" : data.regto,
            "leadto" : data.leadto,
            "mpto" : data.mpto
        })
        return jsonify(status = True, jsonData = jsonData)

@app.route('/bet10/', methods = ['GET', 'POST'])
def bet10():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        data = db.session.query(Bet10).order_by(Bet10.id.desc()).first()
        return render_template('pages/bet10.html', data = data, issues = issues)
    if request.method == 'POST':
        state = request.json["state"]
        if state == "1":
            data = db.session.query(Bet10).order_by(Bet10.id.desc()).first()
            jsonData = []
            jsonData.append({
                "merchant" : data.merchant,
                "impression" : data.impression,
                "click" : data.click,
                "registration" : data.registration,
                "new_deposit" : data.new_deposit,
                "commission" : data.commission,
                "impreytd" : data.impreytd,
                "cliytd" : data.cliytd,
                "regytd" : data.regytd,
                "ndytd" : data.ndytd,
                "commiytd" : data.commiytd
            })
            return jsonify(status = True, jsonData = jsonData)
        elif state == "2":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()
            data = db.session.query(Bet10).filter_by(dateto = dateVal).first()
            if not data:
                return jsonify(status = False, message = "There is no data in your database...?")
            else:
                jsonData = []
                jsonData.append({
                    "merchant" : data.merchant,
                    "impreto" : data.impreto,
                    "clito" : data.clito,
                    "regto" : data.regto,
                    "ndto" : data.ndto,
                    "commito" : data.commito
                })
                return jsonify(status = True, jsonData = jsonData)


@app.route('/realDeal/', methods = ['GET', 'POST'])
def realDeal():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        data = db.session.query(RealDeal).order_by(RealDeal.id.desc()).first()
        return render_template('pages/realDeal.html', data = data, issues = issues)
    if request.method == 'POST':
        state = request.json["state"]
        if state == "1":
            data = db.session.query(RealDeal).order_by(RealDeal.id.desc()).first()
            jsonData = []
            jsonData.append({
                "merchant" : data.merchant,
                "impression" : data.impression,
                "click" : data.click,
                "registration" : data.registration,
                "new_deposit" : data.new_deposit,
                "commission" : data.commission,
                "impreytd" : data.impreytd,
                "cliytd" : data.cliytd,
                "regytd" : data.regiytd,
                "ndytd" : data.ndytd,
                "commiytd" : data.commiytd
            })
            return jsonify(status = True, jsonData = jsonData)
        elif state == "2":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()
            data = db.session.query(RealDeal).filter_by(dateto = dateVal).first()
            if not data:
                return jsonify(status = False, message = "There is no data in your database...?")
            else:
                jsonData = []
                jsonData.append({
                    "merchant" : data.merchant,
                    "impreto" : data.impreto,
                    "clito" : data.clito,
                    "regto" : data.regto,
                    "ndto" : data.ndto,
                    "commito" : data.commito
                })
                return jsonify(status = True, jsonData = jsonData)


@app.route('/ladBroke/')
def ladBroke():
    issues = db.session.query(Log).filter(Log.managed==False).all()
    data = db.session.query(LadBroke).order_by(LadBroke.id.desc()).first()
    return render_template('pages/ladBroke.html', data = data, issues = issues)


@app.route('/betFred/', methods = ['GET', 'POST'])
def betFred():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        data = db.session.query(BetFred).order_by(BetFred.id.desc()).first()
        return render_template('pages/betFred.html', data = data, issues = issues)
    if request.method == 'POST':
        state = request.json["state"]
        if state == "1":
            data = db.session.query(BetFred).order_by(BetFred.id.desc()).first()
            jsonData = []
            jsonData.append({
                "merchant" : data.merchant,
                "impression" : data.impression,
                "click" : data.click,
                "registration" : data.registration,
                "new_deposit" : data.new_deposit,
                "commission" : data.commission,
                "impreytd" : data.impreytd,
                "cliytd" : data.cliytd,
                "regytd" : data.regytd,
                "ndytd" : data.ndytd,
                "commiytd" : data.commiytd
            })
            return jsonify(status = True, jsonData = jsonData)
        elif state == "2":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()
            data = db.session.query(BetFred).filter_by(dateto = dateVal).first()
            if not data:
                return jsonify(status = False, message = "There is no data in your database...?")
            else:
                jsonData = []
                jsonData.append({
                    "merchant" : data.merchant,
                    "impreto" : data.impreto,
                    "clito" : data.clito,
                    "regto" : data.regto,
                    "ndto" : data.ndto,
                    "commito" : data.commito
                })
                return jsonify(status = True, jsonData = jsonData)


@app.route('/paddy/')
def paddy():
    issues = db.session.query(Log).filter(Log.managed==False).all()
    data = db.session.query(Paddy).order_by(Paddy.id.desc()).first()
    return render_template('pages/paddy.html', data = data, issues = issues)


@app.route('/netBet/')
def netBet():
    issues = db.session.query(Log).filter(Log.managed==False).all()
    data = db.session.query(NetBet).order_by(NetBet.id.desc()).first()
    return render_template('pages/netBet.html', data = data, issues = issues)


@app.route('/titanBet/')
def titanBet():
    issues = db.session.query(Log).filter(Log.managed==False).all()
    data = db.session.query(TitanBet).order_by(TitanBet.id.desc()).first()
    return render_template('pages/titanBet.html', data = data, issues = issues)


@app.route('/stan/', methods = ['GET', 'POST'])
def stan():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        data = db.session.query(Stan).order_by(Stan.id.desc()).first()
        return render_template('pages/stan.html', data = data, issues = issues)
    if request.method == 'POST':
        state = request.json["state"]
        if state == "1":
            data = db.session.query(Stan).order_by(Stan.id.desc()).first()
            jsonData = []
            jsonData.append({
                "merchant" : data.merchant,
                "impression" : data.impression,
                "click" : data.click,
                "registration" : data.registration,
                "new_deposit" : data.new_deposit,
                "commission" : data.commission,
                "impreytd" : data.imprytd,
                "cliytd" : data.cliytd,
                "regytd" : data.regytd,
                "ndytd" : data.ndytd,
                "commiytd" : data.commiytd
            })
            return jsonify(status = True, jsonData = jsonData)
        elif state == "2":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()
            data = db.session.query(Stan).filter_by(dateto = dateVal).first()
            if not data:
                return jsonify(status = False, message = "There is no data in your database...?")
            else:
                jsonData = []
                jsonData.append({
                    "merchant" : data.merchant,
                    "impreto" : data.imprto,
                    "clito" : data.clito,
                    "regto" : data.regto,
                    "ndto" : data.ndto,
                    "commito" : data.commito
                })
                return jsonify(status = True, jsonData = jsonData)


@app.route('/coral/', methods = ['GET', 'POST'])
def coral():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        data = db.session.query(Coral).order_by(Coral.id.desc()).first()
        return render_template('pages/coral.html', data = data, issues = issues)
    if request.method == 'POST':
        state = request.json["state"]
        if state == "1":
            data = db.session.query(Coral).order_by(Coral.id.desc()).first()
            jsonData = []
            jsonData.append({
                "merchant" : data.merchant,
                "impression" : data.impression,
                "click" : data.click,
                "registration" : data.registration,
                "new_deposit" : data.new_deposit,
                "commission" : data.commission,
                "impreytd" : data.impreytd,
                "cliytd" : data.cliytd,
                "regytd" : data.regytd,
                "ndytd" : data.ndytd,
                "commiytd" : data.commiytd
            })
            return jsonify(status = True, jsonData = jsonData)
        elif state == "2":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()
            data = db.session.query(Coral).filter_by(dateto = dateVal).first()
            if not data:
                return jsonify(status = False, message = "There is no data in your database...?")
            else:
                jsonData = []
                jsonData.append({
                    "merchant" : data.merchant,
                    "impreto" : data.impreto,
                    "clito" : data.clito,
                    "regto" : data.regto,
                    "ndto" : data.ndto,
                    "commito" : data.commito
                })
                return jsonify(status = True, jsonData = jsonData)


@app.route('/skyBet/', methods = ['GET', 'POST'])
def skyBet():
    data = {}
    if request.method == 'GET':
        issues = db.session.query(Log).filter(Log.managed==False).all()
        data = db.session.query(SkyBet).order_by(SkyBet.id.desc()).first()
        return render_template('pages/skyBet.html', data = data, issues = issues)
    if request.method == 'POST':
        state = request.json["state"]
        if state == "1":
            data = db.session.query(SkyBet).order_by(SkyBet.id.desc()).first()
            jsonData = []
            jsonData.append({
                "merchant" : data.merchant,
                "impression" : data.impression,
                "click" : data.click,
                "registration" : data.registration,
                "new_deposit" : data.new_deposit,
                "commission" : data.commission,
                "impreytd" : data.impreytd,
                "cliytd" : data.cliytd,
                "regytd" : data.regiytd,
                "ndytd" : data.ndytd,
                "commiytd" : data.commiytd
            })
            return jsonify(status = True, jsonData = jsonData)
        elif state == "2":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()
            data = db.session.query(SkyBet).filter_by(dateto = dateVal).first()
            if not data:
                return jsonify(status = False, message = "There is no data in your database...?")
            else:
                jsonData = []
                jsonData.append({
                    "merchant" : data.merchant,
                    "impreto" : data.impreto,
                    "clito" : data.clito,
                    "regto" : data.regito,
                    "ndto" : data.ndto,
                    "commito" : data.commito
                })
                return jsonify(status = True, jsonData = jsonData)


@app.route('/william/')
def william():
    issues = db.session.query(Log).filter(Log.managed==False).all()
    data = db.session.query(William).order_by(William.id.desc()).first()
    return render_template('pages/william.html', data = data, issues = issues)

@app.route('/settings/issues')
def issues():
    issues = db.session.query(Log).filter(Log.managed==False).all()
    return render_template('pages/issues.html', issues = issues)

@app.route('/settings/issues/manage', methods = ["POST"])
def manage_issue():
    id = request.json['id']
    result = db.session.query(Log).filter_by(id = id).update({'managed': True})
    db.session.commit()
    db.session.close()
    return jsonify(status = result)

@app.route('/settings/db', methods = ["GET", "POST"])
def database():
    issues = db.session.query(Log).filter(Log.managed==False).all()
    if request.method == "GET":
        return render_template('pages/db.html', issues = issues)
    else:
        from common.backup import Backup
        me = Backup()
        result = me.dump()
        full_path = result['full_path']
        file_name = result['file_name']
        contents = open(full_path).read().decode("utf-8")
        response = make_response(contents)
        response.headers["Content-Disposition"] = "attachment; filename=%s" % (file_name)
        return response
        # file_name = me.dump()

        # try:
        #     from scrapping.settings.config import PG_BACKUP_PATH
        #     return send_from_directory(PG_BACKUP_PATH, file_name, as_attachment = True)
        #     # return send_file(full_path, as_attachment=True)
        # except Exception as e:
        #     print("Error occured")


@app.route('/victor/', methods = ['GET', 'POST'])
def victor():
    data = {}
    if request.method == 'GET':
        data = db.session.query(Victor).order_by(Victor.id.desc()).first()
        return render_template('pages/victor.html', data = data)
    if request.method == 'POST':
        state = request.json["state"]
        if state == "1":
            data = db.session.query(Victor).order_by(Victor.id.desc()).first()
            jsonData = []
            jsonData.append({
                "merchant" : data.merchant,
                "impression" : data.impression,
                "click" : data.click,
                "registration" : data.registration,
                "new_deposit" : data.new_deposit,
                "commission" : data.commission,
                "impreytd" : data.impreytd,
                "cliytd" : data.cliytd,
                "regytd" : data.regytd,
                "ndytd" : data.ndytd,
                "commiytd" : data.commiytd
            })
            return jsonify(status = True, jsonData = jsonData)
        elif state == "2":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()
            data = db.session.query(Victor).filter_by(dateto = dateVal).first()
            if not data:
                return jsonify(status = False, message = "There is no data in your database...?")
            else:
                jsonData = []
                jsonData.append({
                    "merchant" : data.merchant,
                    "impreto" : data.impreto,
                    "clito" : data.clito,
                    "regto" : data.regto,
                    "ndto" : data.ndto,
                    "commito" : data.commito
                })
                return jsonify(status = True, jsonData = jsonData)



if __name__ == '__main__':
    manager.run()
    # app.debug = True
    # app.run()
