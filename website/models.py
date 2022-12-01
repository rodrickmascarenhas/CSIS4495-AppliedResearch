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
    form_id = db.relationship('Form', backref="Case", lazy="dynamic",foreign_keys="Form.user_id")
    report_id = db.relationship('Report', backref="Reporter", lazy="dynamic",foreign_keys="Report.user_id")

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
    email = db.Column(db.String(120), nullable=False)
    age = db.Column(db.String(60), nullable=False)
    burns = db.Column(db.String(60), nullable=False)
    spread = db.Column(db.String(60), nullable=False)
    diabetes = db.Column(db.Boolean, nullable=False)
    asthma = db.Column(db.Boolean, nullable=False)
    thyroid = db.Column(db.Boolean, nullable=False)
    infection = db.Column(db.Boolean, nullable=False)
    family = db.Column(db.Boolean, nullable=False)
    spot = db.Column(db.String(60), nullable=False)
    color = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(20), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datetime = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    content = db.Column(db.Text, nullable=False)
    note = db.Column(db.Integer, db.ForeignKey('user.id'))
    protected = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))