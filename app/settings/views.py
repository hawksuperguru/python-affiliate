from flask import render_template, url_for, redirect, request, jsonify, make_response
from flask_login import login_required
from . import settings_app as settings
from .. import db as database
from ..models import Log
from pprint import pprint
from .. import get_issues

import datetime, json

@settings.route('/settings/')
@login_required
def index():
    return redirect(url_for("settings.issues"))


@settings.route('/settings/issues')
@login_required
def issues():
    issues = Log.query.filter_by(status = True).all()
    return render_template("settings/issues.html", title = "Issues", issues = issues)

@settings.route('/settings/issues/manage', methods = ["POST"])
@login_required
def manage():
    try:
        id = request.json['id']
        issue = Log.query.filter_by(id = id).first()
        issue.status = False
        database.session.commit()
        
        return jsonify(status = True, message = "Success")
    except:
        return jsonify(status = False, message = "Failure")


@settings.route('/settings/issues/undo', methods = ["POST"])
@login_required
def undo():
    try:
        id = request.json['id']
        issue = Log.query.filter_by(id = id).first()
        issue.status = True
        database.session.commit()
        
        return jsonify(status = True, message = "Success")
    except:
        return jsonify(status = False, message = "Failure")


@settings.route('/settings/db', methods = ['GET', 'POST'])
@login_required
def db():
    if request.method == 'GET':
        issues = get_issues()
        return render_template("settings/db.html", title = "Issues", issues = issues)
    else:
        from ..common.pg_dump import Backup
        me = Backup()
        result = me.dump()
        full_path = result['full_path']
        file_name = result['file_name']
        contents = open(full_path).read().decode("utf-8")
        response = make_response(contents)
        response.headers["Content-Disposition"] = "attachment; filename=%s" % (file_name)
        return response