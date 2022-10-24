from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

auth = Blueprint('auth', __name__)
model = load_model(os.path.join(os.getcwd(), 'cancerdetection.hdf5'))
ALLOWED_EXT = set(['jpg','jpeg','png','jfif'])
classes = {0:"Actinic keratoses",1:"Basal cell carcinoma",2:"Benign keratosis-like lesions",3:"Dermatofibroma",
4:"Melanoma",5:"Melanocytic nevi",6:"Vascular lesions"}

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")


@auth.route('/logout')
def logout():
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")


@auth.route('/health')
def health():
    return render_template("health.html")


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
    target_img = os.path.join('website','static','prediction','images')
    if not os.path.exists(target_img):
        os.makedirs(target_img)
    if request.method != 'POST':
        return render_template("health.html")
    if not request.files:
        flash("Invalid file", category='error')
        return render_template("health.html")
    file = request.files['file']
    if not file or not allowed_file(file.filename):
        flash("Please upload images of jpg, jpeg and png extension only", category='error')
        return render_template("health.html")

    file.save(os.path.join(target_img , file.filename))
    img_path = os.path.join(target_img , file.filename)
    img = file.filename
    factor, probability = predict(img_path,model)

    predictions = {
            "pred1":{"fact1":factor[0],"prob1":probability[0]},
            "pred2":{"fact2":factor[1],"prob2":probability[1]},
            "pred3":{"fact3":factor[2],"prob3": probability[2]}
        }
    return render_template('success.html' , img = img , predictions = predictions)
            