import os
import uuid
import urllib.request
from PIL import Image
from flask import Blueprint,request,render_template,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

auth = Blueprint('auth',__name__)

model = load_model(os.path.join(os.getcwd(), 'cancerdetection.hdf5'))
ALLOWED_EXT = set(['jpg','jpeg','png','jfif'])
classes = {0:"Actinic keratoses",1:"Basal cell carcinoma",2:"Benign keratosis-like lesions",3:"Dermatofibroma",
4:"Melanoma",5:"Melanocytic nevi",6:"Vascular lesions"}

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        Email = request.form.get('email')
        Password = request.form.get('password')
        user = User.query.filter_by(email=Email).first()
        if user:
            if check_password_hash(user.password,Password):
                flash("Logged in successfully", category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again",category='error')
        else:
            flash("Email does not exist.",category='error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        Email = request.form.get('email')
        Fname = request.form.get('firstName')
        Password1 = request.form.get('password1')
        Password2 = request.form.get('password2')
        user = User.query.filter_by(email=Email).first()
        if user:
            flash("Email already exists!", category='error')
        elif len(Email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(Fname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif Password1 != Password2:
            flash('Password don\'t match.', category='error')
        elif len(Password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=Email,fname=Fname,password=generate_password_hash(
                Password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html",user=current_user)

"""Upload API: Some base functions along with main functionality"""
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT

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

@auth.route('/upload',methods=['GET','POST'])
def upload():
    error = ""
    target_img = os.path.join('website','static','images')
    if not os.path.exists(target_img):
        os.mkdir(target_img)
    if request.method == 'POST':
        if (request.form):
            link = request.form.get('link')
            try:
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img, filename)
                url = urllib.request.urlopen(link)
                image = Image.open(url)
                image.save(img_path)
                img = filename
                factor, probability = predict(img_path,model)

                predictions = {
                    "pred1":{"fact1":factor[0],"prob1":probability[0]},
                    "pred2":{"fact2":factor[1],"prob2":probability[1]},
                    "pred3":{"fact3":factor[2],"prob3": probability[2]}
                }    
            
            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'

            if(len(error) == 0):
                return render_template('upload.html' , img = img , predictions = predictions, user=current_user)
            else:
                flash("Image from this site is not accessible or inappropriate input", category='error')
                return render_template("upload.html", user=current_user)
                
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename
                factor, probability = predict(img_path,model)

                predictions = {
                        "pred1":{"fact1":factor[0],"prob1":probability[0]},
                        "pred2":{"fact2":factor[1],"prob2":probability[1]},
                        "pred3":{"fact3":factor[2],"prob3": probability[2]}
                    }

                return render_template('upload.html' , img = img , predictions = predictions, user=current_user)
            else:
                flash("Please upload images of jpg, jpeg and png extension only", category='error')
                return render_template("upload.html", user=current_user)
    else:
        return render_template("upload.html", user=current_user)