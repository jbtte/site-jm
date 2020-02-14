from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    parent = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ammount = db.Column(db.Float)
    operation = db.Column(db.Boolean)
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def current_balance(user_id):
        deposit = db.session.query(func.sum(Balance.ammount)).filter(Balance.user_id==user_id, Balance.operation == True).scalar()
        withdraw = db.session.query(func.sum(Balance.ammount)).filter(Balance.user_id==user_id, Balance.operation == False).scalar()
        return deposit - withdraw

    def account_statement(user_id):
        return db.session.query(Balance).filter(Balance.user_id==user_id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
