from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from website.models import Form
from website import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    if current_user.doctor:
        return render_template('home1.html',profile_pic=profile_pic)
    else:
        return render_template("home.html",profile_pic=profile_pic)

@views.route('/view-form', methods=['GET','POST'])
def view_form():
    form = json.loads(request.data)
    formId = form['formId']
    form = Form.query.get(formId)
    if form:
        return redirect(url_for("auth.view"),formId=formId)
    return jsonify({})

@views.route('/delete-form', methods=['GET','POST'])
def delete_form():
    form = json.loads(request.data)
    formId = form['formId']
    form = Form.query.get(formId)
    if form:
        db.session.delete(form)
        db.session.commit()
    return jsonify({})

@views.route('/send-form', methods=['GET','POST'])
def send_form():
    form = json.loads(request.data)
    formId = form['formId']
    form = Form.query.get(formId)
    if form:
        return redirect(url_for("auth.send"),formId=formId)
    return jsonify({})

@views.route('/add-note', methods=['GET','POST'])
def add_note():
    form = json.loads(request.data)
    formId = form['formId']
    note = form['note']
    form = Form.query.get(formId)
    if form:
        return redirect(url_for("auth.report"),formId=formId,note=note)
    return jsonify({})