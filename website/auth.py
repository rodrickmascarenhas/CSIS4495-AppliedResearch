from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from website import db
import os
import secrets
from .forms import RegisterForm, UpdateForm, LoginForm, RequestResetForm, ResetPasswordForm
from flask_mail import Mail, Message
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

auth = Blueprint('auth', __name__)

model = load_model(os.path.join(os.getcwd(), 'cancerdetection.hdf5'))
ALLOWED_EXT = set(['jpg','jpeg','png','jfif'])
classes = {0:"Actinic keratoses",1:"Basal cell carcinoma",2:"Benign keratosis-like lesions",3:"Dermatofibroma",
4:"Melanoma",5:"Melanocytic nevi",6:"Vascular lesions"}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", 'success')
                profile_pic = url_for('static',filename='images/profile_pics/'+user.image)
                login_user(user,remember=True)
                return redirect(url_for('views.home',profile_pic=profile_pic))
            else:
                flash('Incorrect password. Try again!', 'error')
        else:
            flash('Invalid user. Please sign up!', 'error')
    return render_template("login.html",form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        em = User.query.filter_by(email=email).first()
        if user:
            flash("Username exists. Select different username!")
            return render_template("sign_up.html",form=form)
        if em:
            flash("Email exists. Select different email address!")
            return render_template("sign_up.html",form=form)
        new_user = User(email=email, username=username, password=generate_password_hash(
                password, method='sha256'), length = len(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect (url_for('views.home'))
    return render_template("sign_up.html",form=form)

@auth.route("/edit")
@login_required
def account():
    form = UpdateForm()
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    return render_template("update.html",profile_pic=profile_pic,form=form)

@auth.route("/edit/<params>",methods=['GET','POST'])
@login_required
def edit(params):
    form = UpdateForm()
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    if params == 'username':
        if form.username.data and request.method == 'POST':
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                flash("Username exists. Select different username!",'error')
                return render_template("update.html",profile_pic=profile_pic,form=form)
            else:
                current_user.username = form.username.data
                db.session.commit()
                flash("Username updated successfully!",'success')
                return render_template("update.html",profile_pic=profile_pic,form=form)
        return render_template('update.html',form=form,profile_pic=profile_pic,edit_username=True)
    if params == 'email':
        if form.email.data and request.method == 'POST':
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash("Email exists. Select different email address!",'error')
                return render_template("update.html",profile_pic=profile_pic,form=form)
            else:
                current_user.email = form.email.data
                db.session.commit()
                flash("Email updated successfully!",'success')
                return render_template("update.html",profile_pic=profile_pic,form=form)
        return render_template('update.html',form=form,profile_pic=profile_pic,edit_email=True)
    if params == 'password':
        if form.current.data and form.new.data and request.method == 'POST':
            if check_password_hash(current_user.password, form.current.data):
                current_user.password = generate_password_hash(form.new.data, method='sha256')
                current_user.length = len(form.new.data)
                db.session.commit()
                flash("Password updated successfully!",'success')
                return render_template("update.html",profile_pic=profile_pic,form=form)
            else:
                flash("Current password does not match old password!",'error')
                return render_template("update.html",profile_pic=profile_pic,form=form)
        return render_template('update.html',form=form,profile_pic=profile_pic,edit_password=True)
    if params == 'image':
        if form.image.data and request.method == 'POST':
            random = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.image.data.filename)
            img_fn = random + f_ext
            img_path = os.path.join('website','static','images','profile_pics',img_fn)
            form.image.data.save(img_path)
            current_user.image = img_fn
            db.session.commit()
            flash('Profile picture updated successfully!', 'success')
            profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
            return render_template("update.html",profile_pic=profile_pic,form=form)
        return render_template('update.html',form=form,profile_pic=profile_pic,edit_image=True)
    return render_template("update.html",profile_pic=profile_pic,form=form)

@auth.route('/health')
@login_required
def health():
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    return render_template("health.html", profile_pic=profile_pic)

@auth.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    target_img = os.path.join('website','static','images','test')
    if not os.path.exists(target_img):
        os.makedirs(target_img)
    if request.method == 'POST':
        if not request.files:
            flash("Invalid file", 'error')
            return render_template("health.html", profile_pic=profile_pic)
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            flash("Please upload images of jpg, jpeg and png extension only!", 'error')
            return render_template("health.html", profile_pic=profile_pic)
        else:
            target_img = os.path.join('website','static','images','test')
            file.save(os.path.join(target_img, file.filename))
            img = file.filename
            return render_template("success.html", img=img)

#check if file is supported type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

#load and predict the image for the probability, returns top 3 predictions
def predict(filename , model):
    img = load_img(filename , target_size = (100,75))
    img = img_to_array(img).reshape(1,75,100,3).astype('float32')
    img = img/255.0
    result = model.predict(img)

    dict_result = {}
    probability = []
    factor = []

    for i in range(len(classes)):
        dict_result[result[0][i]] = classes[i]

    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]

    for i in range(3):
        probability.append(round(prob[i]*100,2))
        factor.append(dict_result[prob[i]])

    return factor, probability

# checks if file is appropriate, calls predict() and displays and return with image and predictions
@auth.route('/analyze/<filename>',methods=['GET','POST'])
@login_required
def analyze(filename):
    error = ""
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    target_img = os.path.join('website','static','images','test')
    img_path = os.path.join(target_img , filename)
    factor, probability = predict(img_path,model)

    predictions = {
            "pred1":{"fact1":factor[0],"prob1":probability[0]},
            "pred2":{"fact2":factor[1],"prob2":probability[1]},
            "pred3":{"fact3":factor[2],"prob3": probability[2]}
        }
    return render_template('tool.html' ,img=filename, profile_pic=profile_pic, predictions=predictions)

    """
def generate_reset_token(user):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':user.id)})

def verify_reset_token(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
    except:
        return None
    return User.query.get(user_id)
    """

def send_reset_email(user):
    token = user.generate_reset_token()
    mail = Mail(current_app)
    msg = Message("Account Password Recovery Email!",
    sender=[current_app.config['MAIL_DEFAULT_SENDER']],
    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('.reset_password',token=token,_external=True)}
If you did not make this request then simply ignore this email and no changes will be made
'''
    mail.send(msg)

@auth.route("/reset-password",methods=['GET','POST'])
def reset_request():
    form = RequestResetForm()
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("User does not exist!", 'error')
            return render_template("reset_token.html") 
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", 'success')
        return redirect(url_for('auth.login'))
    return render_template("reset_token.html",form=form)
            
@auth.route("/reset-password/<token>",methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", 'error')
        return redirect(url_for("reset_token"))
    form = ResetPasswordForm()
    if request.method == 'POST':
        user.password = generate_password_hash(form.password.data, method='sha256')
        db.session.commit()
        flash("Your password has been updated. Login with your new password!", 'success')
        return redirect(url_for("auth.login"))
    return render_template("reset_password.html",form=form)