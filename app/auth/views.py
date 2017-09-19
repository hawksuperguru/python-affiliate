from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth_app as auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    """
    Handle requests to create a new acount
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered! You many now login.')

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form = form, title = 'Register')


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    """
    Handle requests to log in
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            return redirect(url_for('home.dashboard'))
        else:
            flash('Invalid email or password.')

    return render_template('auth/login.html', form = form, title = 'Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Hanlde requests to log out
    """
    logout_user()
    flash('You have been logged out.')
    
    return redirect(url_for('auth.login'))