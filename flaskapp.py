from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import json, gc
from functools import wraps
from passlib.handlers.sha2_crypt import sha256_crypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  
from forex_python.converter import CurrencyRates, CurrencyCodes
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/kyan'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'super secret key'

db = SQLAlchemy(app)

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


class Eight88(db.Model):
    __tablename__ = "eight88s"
    id = db.Column(db.Integer, primary_key=True)
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    lead = db.Column(db.Integer)
    money_player = db.Column(db.Integer)
    balance = db.Column(db.Float)

    def __init__(self, impression, click, registration, lead, money_player, balance):
        self.impression = impression
        self.click = click
        self.registration = registration
        self.lead = lead
        self.money_player = money_player
        self.balance = balance


class Bet10(db.Model):
    __tablename__ = "bet10s"
    id = db.Column(db.Integer, primary_key=True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission


class RealDeal(db.Model):
    __tablename__ = "realdeals"
    id = db.Column(db.Integer, primary_key=True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission



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

    def __init__(self, merchant, impression, click, registration, new_deposit, commission):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission


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

    def __init__(self, merchant, impression, click, registration, new_deposit, commission):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission


class Coral(db.Model):
    __tablename__ = "corals"
    id = db.Column(db.Integer, primary_key=True)
    merchant = db.Column(db.String(80))
    impression = db.Column(db.Integer)
    click = db.Column(db.Integer)
    registration = db.Column(db.Integer)
    new_deposit = db.Column(db.Integer)
    commission = db.Column(db.Float)

    def __init__(self, merchant, impression, click, registration, new_deposit, commission):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission


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

    def __init__(self, merchant, impression, click, registration, new_deposit, commission):
        self.merchant = merchant
        self.impression = impression
        self.click = click
        self.registration = registration
        self.new_deposit = new_deposit
        self.commission = commission


class Bet365Other(db.Model):
    __tablename__ = "bet365others"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)
    fromdate = db.Column(db.String(10))
    todate = db.Column(db.String(10))

    def __init__(self, balance, fromdate, todate):
        self.balance = balance
        self.fromdate = fromdate
        self.todate = todate


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
        print(username)
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


@app.route('/dashboard/')
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

    data = [bet365, eight88, bet10, realDeal, ladBroke, betFred, paddy, titanBet, stan, coral, eur, gbp, william, skyBet, netBet, bet365other, valSg]
    return render_template('home.html', data = data)



@app.route('/summary/')
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

    data = [bet365, eight88, bet10, realDeal, ladBroke, betFred, paddy, titanBet, stan, coral, eur, gbp, william, skyBet, netBet, bet365other, valSg]

    return render_template('pages/summary.html', data = data)



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
        print(period)
        fromDate = datetime.datetime.strptime(period.split('-')[0].strip(), '%m/%d/%Y').date()
        toDate = datetime.datetime.strptime(period.split('-')[1].strip(), '%m/%d/%Y').date()
        
        jsonData = []
        if (optVal == '0') or (optVal == '1'):
            data = db.session.query(Bet365).filter(Bet365.dateto >= fromDate).filter(Bet365.dateto <= toDate)
            
            for perDay in data:
                jsonData.append({
                    "dateto" : perDay.dateto,
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


@app.route('/eight88/')
def eight88():
    data = db.session.query(Eight88).order_by(Eight88.id.desc()).first()
    return render_template('pages/eight88.html', data = data)


@app.route('/bet10/')
def bet10():
    data = db.session.query(Bet10).order_by(Bet10.id.desc()).first()
    return render_template('pages/bet10.html', data = data)


@app.route('/realDeal/')
def realDeal():
    data = db.session.query(RealDeal).order_by(RealDeal.id.desc()).first()
    return render_template('pages/realDeal.html', data = data)


@app.route('/ladBroke/')
def ladBroke():
    data = db.session.query(LadBroke).order_by(LadBroke.id.desc()).first()
    return render_template('pages/ladBroke.html', data = data)


@app.route('/betFred/')
def betFred():
    data = db.session.query(BetFred).order_by(BetFred.id.desc()).first()
    return render_template('pages/betFred.html', data = data)


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


@app.route('/stan/')
def stan():
    data = db.session.query(Stan).order_by(Stan.id.desc()).first()
    return render_template('pages/stan.html', data = data)


@app.route('/coral/')
def coral():
    data = db.session.query(Coral).order_by(Coral.id.desc()).first()
    return render_template('pages/coral.html', data = data)


@app.route('/skyBet')
def skyBet():
    data = db.session.query(SkyBet).order_by(SkyBet.id.desc()).first()
    return render_template('pages/skyBet.html', data = data)


@app.route('/william')
def william():
    data = db.session.query(William).order_by(William.id.desc()).first()
    return render_template('pages/william.html', data = data)


@app.route('/bet365other')
def bet365other():
    data = db.session.query(Bet365Other).order_by(Bet365Other.id.desc()).first()
    return render_template('pages/bet365other.html', data = data)


@app.route('/victor')
def victor():
    data = "Woops, credential is not valid. Please tell me account info."
    return render_template('pages/error.html', data = data)


if __name__ == '__main__':
#    app.secret_key = 'super secret key'
#    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run()
