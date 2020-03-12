
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from sqlalchemy import or_
from app import db
import re
import os
import json
from app.main.forms import  get_SearchForm
from app.models import User, Book, Desk, Shelf
from app.main import bp
from fuzzywuzzy import fuzz

@bp.route('/')
@bp.route('/index')
def index():

    return render_template('index.html', title='Landing Page')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    #TODO add functionality to display reserved books in the profile page

    return render_template('user.html', user=user)

#book 
@bp.route('/book/<isbn>')
def book(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()

    return render_template('book_profile.html', book=book)

#book search page
@bp.route('/search', methods=['GET','POST'])
def search():

    form = get_SearchForm()

    if request.method == 'POST':  

        #remove non-alphannumeric characters to prevent sql injections
        query = re.escape(form.q.data)
        query = query.replace(u'\xa0', u' ')

        return redirect(url_for('main.search_results', query=query))

    return render_template('search.html', title = 'search Book', form=form)


#returns the search results from the given query
@bp.route('/search/<query>', methods=['GET', 'POST'])
def search_results(query):
     
    #get books from database
    booksDB = db.session.query(Book).all()
    search_result = dict({})

    for book in booksDB:

        #tokenises the book attributes and uses the levenschtein distance to give each book a score for 
        #   how similar it is to the query
        words = book.title+ " " + book.author + " " + book.subject
        score = fuzz.token_set_ratio(words, query)
        search_result[book] = score

    #sorts the results in descending order
    search_result = sorted(search_result.items(), key=lambda x: x[1], reverse=True)

    print(search_result)
    books = []

    #unpack all the book names into a list, not very elegant but it works 
    for elem in search_result:
        books.append(elem[0])
        
    
    return render_template('search_results.html', books = books[:5])


#confirms that the selected book is the desired one and asks 
# the user to pick a desk to return the book to
@bp.route('/confirm/<isbn>', methods=['GET', 'POST'])
@login_required
def confirm(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()

    if request.method == 'POST':
        desk = request.form['desk']

        return redirect(url_for('main.get', book=book, isbn=isbn ,desk=desk ))

    return render_template('confirm.html', book=book, max=2)




#actually runs the code that gets the book
@bp.route('/get/<isbn>', methods=['GET', 'POST'])
@login_required
def get(isbn):
    
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    user = current_user

    desk_number = request.args.get('desk')
    desk = Desk.query.filter_by(id=desk_number).first()
    
    desk_dict = row2dict(desk)

    print(desk_dict)
    
    print (desk)
    desk_json = json.dumps(desk_dict)

    #open connection to navigation stuff
    #send the the json data 
    #close connection


    label = book.label
    shelf = book.shelf 

    return render_template('get.html', book=book)


def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d



@bp.route('/home', methods=['GET', 'POST'])#might not need post
@login_required
def home(): 
    return render_template('home.html', title = 'Home Page')


@bp.route('/pickup', methods=['GET', 'POST'])
@login_required
def pickup():
    return render_template('pickup.html', title = "Pick Up")


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = get_SearchForm()
