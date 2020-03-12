
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


@bp.route('/home', methods=['GET', 'POST'])#might not need post
@login_required
def home(): 
    return render_template('home.html', title = 'Home Page')



"""
Profile page for the users, here they will be able to view books they have reserved or checked out
"""
@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    
    #TODO add functionality to display reserved books in the profile page

    return render_template('user.html', user=user)



"""
Profile page for the books, here users can reserve or checkout a book
"""
@bp.route('/book/<isbn>')
def book(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()
    return render_template('book_profile.html', book=book)



"""
Search page, users input a query and this page forwards that query to the search)results page

"""
@bp.route('/search', methods=['GET','POST'])
def search():

    form = get_SearchForm()

    #if the user has entered a query then pass data to the search_results page
    if request.method == 'POST':  

        #remove non-alphannumeric characters to prevent sql injections
        query = re.escape(form.q.data)
        query = query.replace(u'\xa0', u' ')

        return redirect(url_for('main.search_results', query=query))

    return render_template('search.html', title = 'search Book', form=form)



"""
This page displays results based on the user query
"""
@bp.route('/search/<query>', methods=['GET', 'POST'])
def search_results(query):
     
    #get books from database
    booksDB = db.session.query(Book).all()
    search_result = dict({})

    for book in booksDB:

        #tokenises the book attributes and uses the levenschtein distance to give each book a score for 
        #   how similar it is to the query
        #TODO this is okay but still a bit shit, doesnt do well with typos

        words = book.title+ " " + book.author + " " + book.subject
        score = fuzz.token_set_ratio(words, query)
        search_result[book] = score

    #sorts the results in descending order
    search_result = sorted(search_result.items(), key=lambda x: x[1], reverse=True)

    books = []
    #unpack all the book names into a list, not very elegant but it works 
    for elem in search_result:
        books.append(elem[0])
        
    return render_template('search_results.html', books = books[:5])



"""
Confirms that the selected book is the desired one and asks the user to pick a desk to return the book to
"""
@bp.route('/confirm/<isbn>', methods=['GET', 'POST'])
@login_required
def confirm(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()

    if request.method == 'POST':
        desk = request.form['desk']

        #passing the isbn here is bit redundant but am too dumb to get it to work another way
        return redirect(url_for('main.get', book=book, isbn=isbn ,desk=desk ))

    return render_template('confirm.html', book=book, max=2)



"""
Finally, runs the code that actually gets the book :P
"""
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



"""
one helpy boi
"""
def row2dict(row):
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))

        return d



#TODO
@bp.route('/pickup', methods=['GET', 'POST'])
@login_required
def pickup():
    return render_template('pickup.html', title = "Pick Up")


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = get_SearchForm()
