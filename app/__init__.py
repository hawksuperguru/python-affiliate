from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from apscheduler.scheduler import Scheduler

import logging

db = SQLAlchemy()
login_manager = LoginManager()
scheduler = Scheduler()

def create_app(config_name = "dev"):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app import models

    # from .admin import admin_app
    from .auth import auth_app
    from .home import home_app
    from .settings import settings_app

    # app.register_blueprint(admin_app, url_prefix='/admin')
    app.register_blueprint(auth_app)
    app.register_blueprint(home_app)
    app.register_blueprint(settings_app)

    from .spiders import Spider
    scheduler.app = app
    logging.basicConfig()

    def scrap_affiliates():
        print("=========================================")
        print("Scheduled Jobs are bing started shortly...")
        spider = Spider()
        spider.run()

    scheduler.start()
    scheduler.add_cron_job(scrap_affiliates, hours = 3)

    return app

def get_issues():
    from .models import Log
    return Log.query.filter_by(status = True).all()