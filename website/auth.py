from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import User, Form
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from website import db
import os
import secrets
import uuid
import sqlalchemy as db_alchemy
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
    if not User.query.filter_by(doctor=1).all():
        insert_docs()
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        if request.form.get('user') == 'User':
            user = User.query.filter_by(email=email).first()
            if user and not user.doctor:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", 'success')
                    login_user(user,remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password. Try again!', 'error')
            else:
                flash('Unidentified sign-in! Please sign up!', 'error')
        elif request.form.get('doctor') == 'Doctor':
            user = User.query.filter_by(email=email).first()
            if user and user.doctor:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully!", 'success')
                    login_user(user,remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password. Try again!','error')
            else:
                flash("Unidentified sign-in! Check your credentials!", 'error')
        else:
            flash('Invalid user. Please sign up!', 'error')
    return render_template("login.html",form=form)

# bulk insert records
def insert_docs():
    db.session.add(User(email="johnq@gmail.com", username="Dr. John Q", password=generate_password_hash(
                "johnquasimoto", method='sha256'), doctor=True, length = len("johnquasimoto"), fee=210))
    db.session.add(User(email="jackiec@gmail.com", username="Dr. Jackie C", password=generate_password_hash(
                        "jackieconnelly", method='sha256'), doctor=True, length = len("jackieconnelly"), fee=245))
    db.session.add(User(email="timg@gmail.com", username="Dr. Tim G", password=generate_password_hash(
                        "timgrayson", method='sha256'), doctor=True, length = len("timgrayson"), fee=235))
    db.session.commit()
    
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
            flash("Username exists. Select different username!",'error')
            return render_template("sign_up.html",form=form)
        if em:
            flash("Email exists. Select different email address!",'error')
            return render_template("sign_up.html",form=form)
        new_user = User(email=email, username=username, password=generate_password_hash(
                password, method='sha256'), length=len(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('views.home'))
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
    doctors = User.query.filter_by(doctor=True)
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    return render_template("health.html",doctors=doctors,profile_pic=profile_pic)

@auth.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    if current_user.doctor == True:
        return redirect(url_for("views.home"))
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    target_img = os.path.join('website','static','images','test')
    if not os.path.exists(target_img):
        os.makedirs(target_img)
    if request.method == 'POST':
        if request.form.get('gender') is None or request.form.get('age') is None or request.form.get('skinBurn') is None or request.form.get('skinMole') is None or request.form.get('familyHistory') is None or request.form.get('simDisease') is None or request.form.get('result') == "" or request.form.get('area') == "" or request.form.get('color') == "" or request.form.get('doctor') is None:
            flash("Please fill all appropriate responses","error")
            return render_template("health.html", profile_pic=profile_pic)
        if not request.files:
            flash("Invalid file!", 'error')
        file = request.files['file']
        if not file or not allowed_file(file.filename):
            flash("Please upload images of jpg, jpeg and png extension only!", 'error')
            return render_template("health.html", profile_pic=profile_pic)
        else:
            img = file.filename
            encoder = str(uuid.uuid4())
            _, f_ext = os.path.splitext(img)
            img = encoder + f_ext
            img_path = os.path.join(target_img,img)
            form = Form(gender=request.form.get('gender'),age=request.form.get('age'),
            burns=request.form.get('skinBurn'), spread=request.form.get('skinMole'),
            diabetes=(request.form.get('Diabetes')=="Diabetes"), asthma=(request.form.get('Asthma')=="Asthma"),
            thyroid=(request.form.get('Thyroid')=="Thyroid"), infection=(request.form.get('BloodInfection')=="BloodInfection"),
            family=(request.form.get('familyHistory')=="familyYes"), spot=request.form.get('area'),
            issue=(request.form.get('simDisease')=="simYes"), risk=request.form.get('result'),
            doctor_id=request.form.get('doctor'),protected=False, content="",
            color=request.form.get('color'), image=img, user_id=current_user.id)
            db.session.add(form)
            db.session.commit()
            file.save(img_path)
            return render_template("success.html",img=img,form=form,profile_pic=profile_pic)
    return render_template("health.html",profile_pic=profile_pic)

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
    if current_user.doctor == True:
        return redirect(url_for("views.home"))
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    target_img = os.path.join('website','static','images','test')
    img_path = os.path.join(target_img, filename)
    factor, probability = predict(img_path,model)
    return render_template('tool.html', img=filename, profile_pic=profile_pic, fact=factor, prob=probability)

"""def generate_reset_token(user):
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
        
@auth.route("/form")
@login_required
def form():
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    if current_user.doctor:
        query = db_alchemy.select(['*']).where(db_alchemy.and_(Form.doctor_id == current_user.id,Form.protected==True)).order_by(db_alchemy.asc(Form.datetime))
    else:
        query = db_alchemy.select(['*']).where(db_alchemy.and_(Form.user_id == current_user.id)).order_by(db_alchemy.asc(Form.datetime))
        """query = db_alchemy.select([User.email,User.username]).where(db_alchemy.and_(User.username=='rodrick'))"""
    forms = db.session.execute(query)
    users = User.query.all()
    return render_template("forms.html",users=users,forms=forms,profile_pic=profile_pic)

@auth.route("/form/<formId>")
@login_required
def view(formId):
    form = Form.query.filter_by(id=formId).first()
    user = User.query.filter_by(id=form.user_id).first()
    doc = User.query.filter_by(id=form.doctor_id).first()
    img_path = os.path.join('website','static','images','test',form.image)
    factor, probability = predict(img_path,model)
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    return render_template("docu.html",user=user,doc=doc,form=form,fact=factor,prob=probability,profile_pic=profile_pic)

@auth.route('/send/<formId>')
def send(formId):
    form = Form.query.filter_by(id=formId).first()
    user = User.query.filter_by(id=form.user_id).first()
    doc = User.query.filter_by(id=form.doctor_id).first()
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    form.protected = True
    db.session.commit()
    return render_template("success1.html",user=user,doc=doc,form=form,profile_pic=profile_pic)       

@auth.route('/report/<formId>/<note>')
def report(formId,note):
    form = Form.query.filter_by(id=formId).first()
    user = User.query.filter_by(id=form.user_id).first()
    doc = User.query.filter_by(id=form.doctor_id).first()
    profile_pic = url_for('static',filename='images/profile_pics/'+current_user.image)
    if len(note)<10:
        flash("Note is too short. Please describe the solution as clearly possible!","error")
        return redirect(url_for("auth.view",formId=formId))
    form.content = note
    db.session.commit()
    return render_template("success1.html",user=user,doc=doc,form=form,profile_pic=profile_pic)