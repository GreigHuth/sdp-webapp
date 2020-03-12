from hashlib import md5
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login




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

    def avatar(self):
        return md5(self.username.encode('utf8')).hexdigest
        
    #describes how to print the class
    def __repr__(self):
        return '<User {}>'.format(self.username) 


class Desk(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, index=True)
    y = db.Column(db.Float)
    angle = db.Column(db.Float)

    def __repr__(self):
        return '<Desk {}>'.format(self.id)

class Shelf(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, index=True)
    y = db.Column(db.Float)
    angle = db.Column(db.Float)

#SQL Schema for Book Table
class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), index=True, unique=True)
    author = db.Column(db.String(64)) 
    label = db.Column(db.String(16))#LOC label on the book
    subject = db.Column(db.String(64))
    isbn = db.Column(db.String(16))
    holder = db.Column(db.Integer, db.ForeignKey('user.id'))# id of the user that has the book
    shelf = db.Column(db.Integer, db.ForeignKey('shelf.id'))# shelf the book is on
    

    def __repr__(self):
        return '<Book {}>'.format(self.title)

    def get_pic(self):
        return "https://pictures.abebooks.com/isbn/"+str(self.isbn)+"-uk-300.jpg"

    def get_label(self, book):
        label = self.query.filter_by(name=book).first()
        return label.label

    # registers book ownership to
    def reserve_book(self, user):
        self.holder = user.id

    def reserved(self):
        if self.holder == "":
            return False;
        else:
            return True;

#dunno how this works yet but tbh its not that important rn

#gets unique session id for the users that logged in
@login.user_loader
def load_user(id):
    return User.query.get(int(id))