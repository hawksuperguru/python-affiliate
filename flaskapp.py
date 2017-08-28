from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/kyan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def datetimeformat(value, format='%Y/%m'):
    return value.strftime(format)

jinja2.filters.FILTERS['datetimeformat'] = datetimeformat


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


    def __init__(self, impression, click, registration, lead, money_player, balance, prebalance, imprwk, cliwk, regwk, leadwk, mpwk, imprpre, clipre, regpre, leadpre, mppre, imprto, clito, regto, leadto, mpto):
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


class Bet10(db.Model):
    __tablename__ = "bet10s"
    id = db.Column(db.Integer, primary_key=True)
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
    dateto = db.Column(db.Date, unique = True)

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
    dateto = db.Column(db.Date, unique = True)

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
    balance = db.Column(db.Float)

    def __init__(self, balance):
        self.balance = balance


class BetFred(db.Model):
    __tablename__ = "betfreds"
    id = db.Column(db.Integer, primary_key=True)
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
    dateto = db.Column(db.Date, unique = True)

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
    balance = db.Column(db.Float)

    def __init__(self, balance):
        self.balance = balance


class NetBet(db.Model):
    __tablename__ = "netbets"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)

    def __init__(self, balance):
        self.balance = balance


class TitanBet(db.Model):
    __tablename__ = "titanbets"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)

    def __init__(self, balance):
        self.balance = balance


class Stan(db.Model):
    __tablename__ = "stans"
    id = db.Column(db.Integer, primary_key=True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)
    imprytd = db.Column(db.Integer)
    cliytd = db.Column(db.Integer)
    regytd = db.Column(db.Integer)
    ndytd = db.Column(db.Integer)
    commiytd = db.Column(db.Float)
    imprto = db.Column(db.Integer)
    clito = db.Column(db.Integer)
    regto = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)
    dateto = db.Column(db.Date, unique = True)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission, imprytd, cliytd, regytd, ndytd, commiytd, imprto, clito, regto, ndto, commito, dateto):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission
        self.imprytd = imprytd
        self.cliytd = cliytd
        self.regytd = regytd
        self.ndytd = ndytd
        self.commiytd = commiytd
        self.imprto = imprto
        self.clito = clito
        self.regto = regto
        self.ndto = ndto
        self.commito = commito
        self.dateto = dateto


class Coral(db.Model):
    __tablename__ = "corals"
    id = db.Column(db.Integer, primary_key=True)
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
    dateto = db.Column(db.Date, unique = True)

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


class William(db.Model):
    __tablename__ = "williams"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)

    def __init__(self, balance):
        self.balance = balance


class SkyBet(db.Model):
    __tablename__ = "skybets"
    id = db.Column(db.Integer, primary_key=True)
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
    regito = db.Column(db.Integer)
    ndto = db.Column(db.Integer)
    commito = db.Column(db.Float)
    dateto = db.Column(db.Date, unique = True)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission, impreytd, cliytd, regiytd, ndytd, commiytd, impreto, clito, regito, ndto, commito, dateto):
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
        self.regito = regito
        self.ndto = ndto
        self.commito = commito
        self.dateto = dateto


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

        # (data[5].commission * data[11])|round(2, 'floor') + data[9].commission + data[8].commission + (data[13].commission * data[11])|round(2, 'floor') + (data[3].commission * data[10])|round(2, 'floor') + (data[2].commission * data[10])|round(2, 'floor') + data[0].ndepo + data[15].ndepo * 100 + data[1].balance + (data[12].balance * data[10])|round(2, 'floor') + (data[4].balance * data[11])|round(2, 'floor') + (data[6].balance * data[10])|round(2, 'floor') + (data[14].balance * data[10])|round(2, 'floor') + data[7].balance

        # totalSum = betFred.commission * gbp + coral.commission + stan.commission + skyBet.commission * gbp + realDeal.commission * eur + bet10.commission * eur + bet365Data.ndepo * 100 + bet365otherData.ndepo * 100 + eight88.balance + william.balance * eur + ladBroke.balance * gbp + paddy.balance * eur + netBet.balance * eur + titanBet.balance
       
        data = [bet365Data, eight88, bet10, realDeal, ladBroke, betFred, paddy, titanBet, stan, coral, eur, gbp, william, skyBet, netBet, bet365otherData, valSg]

        return render_template('pages/summary.html', data = data)

    if request.method == 'POST':
        val = request.json['val']
        state = request.json['state']
        if state == "1":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()

            bet365 = db.session.query(Bet365).filter_by(dateto = dateVal).first()
            bet10 = db.session.query(Bet10).filter_by(dateto = dateVal).first()
            realDeal = db.session.query(RealDeal).filter_by(dateto = dateVal).first()
            betFred = db.session.query(BetFred).filter_by(dateto = dateVal).first()
            stan = db.session.query(Stan).filter_by(dateto = dateVal).first()
            coral = db.session.query(Coral).filter_by(dateto = dateVal).first()
            skyBet = db.session.query(SkyBet).filter_by(dateto = dateVal).first()
            bet365other = db.session.query(Bet365Other).filter_by(dateto = dateVal).first()
            # if not (betFred) or (bet10) or (realDeal) or (betFred) or (stan) or (coral) or (skyBet) or (bet365other):
            #     return jsonify(status = False, message = "There is no data in your database...?")


            tB3Odollar = bet365other.ndepo * 100
            tB3dollar = bet365.ndepo * 100
            tB10dollar = "%.2f" % round(bet10.commito * eur, 2)
            tRealdollar = "%.2f" % round(realDeal.commito * eur, 2)
            tSkydollar = "%.2f" % round(skyBet.commito * gbp, 2)
            tStandollar = stan.commito
            tBFdollar = "%.2f" % round(betFred.commito * gbp, 2)
            tWildollar = "%.2f" % round(william.balance * eur, 2)
            tLadollar = "%.2f" % round(ladBroke.balance * gbp, 2)
            tPadollar = "%.2f" % round(paddy.balance * eur, 2)
            tNetdollar = "%.2f" % round(netBet.balance * eur, 2)

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

                "tB10click" : bet10.clito,
                "tB10register" : bet10.regto,
                "tB10commission" : bet10.commito,
                "tB10dollar" : tB10dollar,

                "tRealclick" : realDeal.clito,
                "tRealregister" : realDeal.regto,
                "tRealcommission" : realDeal.commito,
                "tRealdollar" : tRealdollar,

                "tSkyclick" : skyBet.clito,
                "tSkyregister" : skyBet.regito,
                "tSkycommission" : skyBet.commito,
                "tSkydollar": tSkydollar,

                "tWildollar" : tWildollar,
                
                "tLadollar" : tLadollar,
                
                "tPadollar" : tPadollar,
                
                "tNetdollar" : tNetdollar,
                
                "tTidollar" : titanBet.balance,

                "tStanclick" : stan.clito,
                "tStanregister" : stan.regto,
                "tStancommission" : stan.commito,
                "tStandollar" : tStandollar,

                "tCoralclick" : coral.clito,
                "tCoralregister" : coral.regto,
                "tCoralcommission" : coral.commito,
                "tCoraldollar" : coral.commito,

                "tBFclick" : betFred.clito,
                "tBFregister" : betFred.regto,
                "tBFcommission" : betFred.commito,
                "tBFdollar" : tBFdollar,

                # "total" : total
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
                tWildollar = "%.2f" % round(william.balance * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.balance * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.balance * eur, 2)

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
                tWildollar = "%.2f" % round(william.balance * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.balance * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.balance * eur, 2)

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
                    "tSkyregister" : skyBet.regiytd,
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

        # (data[5].commission * data[11])|round(2, 'floor') + data[9].commission + data[8].commission + (data[13].commission * data[11])|round(2, 'floor') + (data[3].commission * data[10])|round(2, 'floor') + (data[2].commission * data[10])|round(2, 'floor') + data[0].ndepo + data[15].ndepo * 100 + data[1].balance + (data[12].balance * data[10])|round(2, 'floor') + (data[4].balance * data[11])|round(2, 'floor') + (data[6].balance * data[10])|round(2, 'floor') + (data[14].balance * data[10])|round(2, 'floor') + data[7].balance

        # totalSum = betFred.commission * gbp + coral.commission + stan.commission + skyBet.commission * gbp + realDeal.commission * eur + bet10.commission * eur + bet365Data.ndepo * 100 + bet365otherData.ndepo * 100 + eight88.balance + william.balance * eur + ladBroke.balance * gbp + paddy.balance * eur + netBet.balance * eur + titanBet.balance
       
        data = [bet365Data, eight88, bet10, realDeal, ladBroke, betFred, paddy, titanBet, stan, coral, eur, gbp, william, skyBet, netBet, bet365otherData, valSg]

        return render_template('pages/summary.html', data = data)

    if request.method == 'POST':
        val = request.json['val']
        state = request.json['state']
        if state == "1":
            dateStr = request.json['val']
            dateVal = datetime.datetime.strptime(dateStr, '%m/%d/%Y').date()

            bet365 = db.session.query(Bet365).filter_by(dateto = dateVal).first()
            bet10 = db.session.query(Bet10).filter_by(dateto = dateVal).first()
            realDeal = db.session.query(RealDeal).filter_by(dateto = dateVal).first()
            betFred = db.session.query(BetFred).filter_by(dateto = dateVal).first()
            stan = db.session.query(Stan).filter_by(dateto = dateVal).first()
            coral = db.session.query(Coral).filter_by(dateto = dateVal).first()
            skyBet = db.session.query(SkyBet).filter_by(dateto = dateVal).first()
            bet365other = db.session.query(Bet365Other).filter_by(dateto = dateVal).first()
            # if not (betFred) or (bet10) or (realDeal) or (betFred) or (stan) or (coral) or (skyBet) or (bet365other):
            #     return jsonify(status = False, message = "There is no data in your database...?")


            tB3Odollar = bet365other.ndepo * 100
            tB3dollar = bet365.ndepo * 100
            tB10dollar = "%.2f" % round(bet10.commito * eur, 2)
            tRealdollar = "%.2f" % round(realDeal.commito * eur, 2)
            tSkydollar = "%.2f" % round(skyBet.commito * gbp, 2)
            tStandollar = stan.commito
            tBFdollar = "%.2f" % round(betFred.commito * gbp, 2)
            tWildollar = "%.2f" % round(william.balance * eur, 2)
            tLadollar = "%.2f" % round(ladBroke.balance * gbp, 2)
            tPadollar = "%.2f" % round(paddy.balance * eur, 2)
            tNetdollar = "%.2f" % round(netBet.balance * eur, 2)

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

                "tB10click" : bet10.clito,
                "tB10register" : bet10.regto,
                "tB10commission" : bet10.commito,
                "tB10dollar" : tB10dollar,

                "tRealclick" : realDeal.clito,
                "tRealregister" : realDeal.regto,
                "tRealcommission" : realDeal.commito,
                "tRealdollar" : tRealdollar,

                "tSkyclick" : skyBet.clito,
                "tSkyregister" : skyBet.regito,
                "tSkycommission" : skyBet.commito,
                "tSkydollar": tSkydollar,

                "tWildollar" : tWildollar,
                
                "tLadollar" : tLadollar,
                
                "tPadollar" : tPadollar,
                
                "tNetdollar" : tNetdollar,
                
                "tTidollar" : titanBet.balance,

                "tStanclick" : stan.clito,
                "tStanregister" : stan.regto,
                "tStancommission" : stan.commito,
                "tStandollar" : tStandollar,

                "tCoralclick" : coral.clito,
                "tCoralregister" : coral.regto,
                "tCoralcommission" : coral.commito,
                "tCoraldollar" : coral.commito,

                "tBFclick" : betFred.clito,
                "tBFregister" : betFred.regto,
                "tBFcommission" : betFred.commito,
                "tBFdollar" : tBFdollar,

                # "total" : total
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
                tWildollar = "%.2f" % round(william.balance * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.balance * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.balance * eur, 2)

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
                tWildollar = "%.2f" % round(william.balance * eur, 2)
                tLadollar = "%.2f" % round(ladBroke.balance * gbp, 2)
                tPadollar = "%.2f" % round(paddy.balance * eur, 2)
                tNetdollar = "%.2f" % round(netBet.balance * eur, 2)

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
                    "tSkyregister" : skyBet.regiytd,
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
        return render_template('pages/bet365.html', data = data)

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
        now = datetime.datetime.now()
        today = now.date()
        data = db.session.query(Bet365Other).filter(Bet365Other.dateto == today)
        return render_template('pages/bet365other.html', data = data)

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
        data = db.session.query(Eight88).order_by(Eight88.id.desc()).first()
        return render_template('pages/eight88.html', data = data)
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
        data = db.session.query(Bet10).order_by(Bet10.id.desc()).first()
        return render_template('pages/bet10.html', data = data)
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
        data = db.session.query(RealDeal).order_by(RealDeal.id.desc()).first()
        return render_template('pages/realDeal.html', data = data)
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
    data = db.session.query(LadBroke).order_by(LadBroke.id.desc()).first()
    return render_template('pages/ladBroke.html', data = data)


@app.route('/betFred/', methods = ['GET', 'POST'])
def betFred():
    data = {}
    if request.method == 'GET':
        data = db.session.query(BetFred).order_by(BetFred.id.desc()).first()
        return render_template('pages/betFred.html', data = data)
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
    data = db.session.query(Paddy).order_by(Paddy.id.desc()).first()
    return render_template('pages/paddy.html', data = data)


@app.route('/netBet/')
def netBet():
    data = db.session.query(NetBet).order_by(NetBet.id.desc()).first()
    return render_template('pages/netBet.html', data = data)


@app.route('/titanBet/')
def titanBet():
	# data = db.session.query(TitanBet).all()[1]
    data = db.session.query(TitanBet).order_by(TitanBet.id.desc()).first()
    return render_template('pages/titanBet.html', data = data)


@app.route('/stan/', methods = ['GET', 'POST'])
def stan():
    data = {}
    if request.method == 'GET':
        data = db.session.query(Stan).order_by(Stan.id.desc()).first()
        return render_template('pages/stan.html', data = data)
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
        data = db.session.query(Coral).order_by(Coral.id.desc()).first()
        return render_template('pages/coral.html', data = data)
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
        data = db.session.query(SkyBet).order_by(SkyBet.id.desc()).first()
        return render_template('pages/skyBet.html', data = data)
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
    data = db.session.query(William).order_by(William.id.desc()).first()
    return render_template('pages/william.html', data = data)


@app.route('/victor/')
def victor():
    data = "Woops, credential is not valid. Please tell me account info."
    return render_template('pages/error.html', data = data)


if __name__ == '__main__':
    # manager.run()
    app.debug = True
    app.run()
