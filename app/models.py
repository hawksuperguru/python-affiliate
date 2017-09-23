from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Role(db.Model):
    """
    Roles Table
    """
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40), unique = True)
    description = db.Column(db.String(200))
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class User(UserMixin, db.Model):
    """
    Users Table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(60), index = True, unique = True)
    username = db.Column(db.String(60), index = True, unique = True)
    firstname = db.Column(db.String(40))
    lastname = db.Column(db.String(40))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.Column(db.Boolean, default = False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Affiliate(db.Model):
    """
    Affiliates table
    """
    __tablename__ = 'affiliates'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(60), index = True, unique = True)
    histories = db.relationship("History", backref="history", lazy="dynamic")

    def __repr__(self):
        return '<Affiliate: {}>'.format(self.name)

class History(db.Model):
    """
    Histories table
    """
    __tablename__ = 'histories'

    id = db.Column(db.Integer, primary_key = True)
    affiliate_id = db.Column(db.Integer, db.ForeignKey('affiliates.id'))
    daily_click = db.Column(db.Integer, default = 0)
    daily_signup = db.Column(db.Integer, default = 0)
    daily_commission = db.Column(db.Float, default = 0.0)
    weekly_click = db.Column(db.Integer, default = 0)
    weekly_signup = db.Column(db.Integer, default = 0)
    weekly_commission = db.Column(db.Float, default = 0.0)
    monthly_click = db.Column(db.Integer, default = 0)
    monthly_signup = db.Column(db.Integer, default = 0)
    monthly_commission = db.Column(db.Float, default = 0.0)
    yearly_click = db.Column(db.Integer, default = 0)
    yearly_signup = db.Column(db.Integer, default = 0)
    yearly_commission = db.Column(db.Float, default = 0.0)
    paid_signup = db.Column(db.Integer, default = 0)
    created_at = db.Column(db.Date)
    affiliate = db.relationship(Affiliate, backref = 'affiliates')

    def __repr__(self):
        return '<History: {} {}>'.format(self.affiliate_id, self.created_at)

    @property
    def serialize(self):
        """Return object data in easily serializeable format."""
        return {
            id : self.id,
            affiliate_id: self.affiliate_id,
            daily_click: self.daily_click,
            daily_signup: self.daily_signup,
            daily_commission: self.daily_commission,
            weekly_click: self.weekly_click,
            weekly_signup: self.weekly_signup,
            weekly_commission: self.weekly_commission,
            monthly_click: self.monthly_click,
            monthly_signup: self.monthly_signup,
            monthly_commission: self.monthly_commission,
            yearly_click: self.yearly_click,
            yearly_signup: self.yearly_signup,
            yearly_commission: self.yearly_commission,
            paid_signup: self.paid_signup,
            created_at: self.created_at,
        }


class Log(db.Model):
    """
    Exception logs table
    """
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key = True)
    affiliate = db.Column(db.String(50))
    message = db.Column(db.String(200))
    created_at = db.Column(db.Date)

    def __repr__(self):
        return '<Log: {}>'.format(self.affiliate_id)