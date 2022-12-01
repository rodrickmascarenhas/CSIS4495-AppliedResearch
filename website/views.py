from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_required, current_user
from website.models import Form
from website import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    return render_template("home.html",profile_pic=profile_pic,current_user=current_user)

@views.route('/delete-form', methods=['POST'])
def delete_form():
    form = json.loads(request.data)
    formId = form['formId']
    form = Form.query.get(formId)
    if form:
        db.session.delete(form)
        db.session.commit()
    return jsonify({})
