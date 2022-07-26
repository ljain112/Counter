from app import db, login
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
                                                                                                                                                                                                                                          






class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    entrys = db.relationship('Entry', backref='author', lazy='dynamic',order_by='Entry.date')


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return  check_password_hash(self.password_hash, password)


class Entry(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    date = db.Column(db.DateTime, index=True, default=dt.utcnow)
    timestamp = db.Column(db.DateTime, index=True, default=dt.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Entry {}>'.format(self.id) 





@login.user_loader
def load_user(id):
    return User.query.get(int(id))
