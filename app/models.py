from app import db
#each class represents a table in the database

class User(db.Model):

    userId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    #describes how to print the class
    def __repr__(self):
        return '<User {}>'.format(self.username) 

class Book(db.Model):
    bookId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    author = db.Column(db.String(64))
    holder = db.Column(db.Integer, db.ForeignKey('user.userId'))

    def __repr__(self):
        return '<Book {}>'.format(self.name)