from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#each class represents a table in the database

# SQL schema for User Table
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #books = db.relationship('Book', backref='holder', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    #returns true if the passwords match, false otherwise
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    #describes how to print the class
    def __repr__(self):
        return '<User {}>'.format(self.username) 

#SQL Schema for Book Table
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    author = db.Column(db.String(64))
    holder = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.name)
#gets unique session id for the users that logged in
@login.user_loader
def load_user(id):
    return User.query.get(int(id))