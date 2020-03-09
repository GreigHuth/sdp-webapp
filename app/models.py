from hashlib import md5
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from app.search import add_to_index, remove_from_index, query_index

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

    def avatar(self):
        return md5(self.username.encode('utf8')).hexdigest
        
    #describes how to print the class
    def __repr__(self):
        return '<User {}>'.format(self.username) 

#SQL Schema for Book Table
class Book(SearchableMixin, db.Model):
    __searchable__ = ['title']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), unique=True,)
    author = db.Column(db.String(64)) 
    label = db.Column(db.String(16), unique=True)#LOC label on the book
    subject = db.Column(db.String(64))
    holder = db.Column(db.Integer, db.ForeignKey('user.id'))# id of the user that has the book
    shelf = db.Column(db.Integer)# shelf the book is on

    def __repr__(self):
        return '<Book {}>'.format(self.name)

    def get_label(self, book):
        label = self.query.filter_by(name=book).first()
        return label.label


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

#gets unique session id for the users that logged in
@login.user_loader
def load_user(id):
    return User.query.get(int(id))