from flask import Blueprint, render_template, request, jsonify, url_for
from flask_login import login_required, current_user
from website.models import Post
from website import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    """if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash("Note is too short",category="error")
        else:
            new_note = Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added",category="success")
    """
    return render_template("home.html",profile_pic=profile_pic,current_user=current_user)


@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        db.session.delete(post)
        db.session.commit()
    return jsonify({})
