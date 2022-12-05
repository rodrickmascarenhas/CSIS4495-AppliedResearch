from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from website import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    doctor = db.Column(db.Boolean, nullable=False, default=False)
    fee = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(20), nullable=False, default="default.png")
    user_id = db.relationship('Form', backref="Case", lazy="dynamic",foreign_keys="Form.user_id")

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image}','{self.posts}')"

    def generate_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id})

    def verify_reset_token(self,token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(60), nullable=False)
    age = db.Column(db.String(60), nullable=False)
    burns = db.Column(db.String(60), nullable=False)
    spread = db.Column(db.String(60), nullable=False)
    diabetes = db.Column(db.Boolean, nullable=False)
    asthma = db.Column(db.Boolean, nullable=False)
    thyroid = db.Column(db.Boolean, nullable=False)
    infection = db.Column(db.Boolean, nullable=False)
    family = db.Column(db.Boolean, nullable=False)
    issue = db.Column(db.Boolean, nullable=False)
    risk = db.Column(db.Integer, nullable=False)
    spot = db.Column(db.String(60), nullable=False)
    color = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String(200), nullable=True)
    protected = db.Column(db.Boolean, default=False)