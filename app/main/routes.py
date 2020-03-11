
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from sqlalchemy import or_
from app import db
import re
from app.main.forms import  get_SearchForm
from app.models import User, Book
from app.main import bp
from fuzzywuzzy import fuzz
from jellyfish import levenshtein_distance as ld 

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

@bp.route('/book/<isbn>')
@login_required
def book(isbn):
    book = Book.query.filter_by(isbn=isbn).first_or_404()

    return render_template('book_profile.html', book=book)

@bp.route('/search', methods=['GET','POST'])
@login_required
def search():

    form = get_SearchForm()
    if request.method == 'POST':  
        query = re.escape(form.q.data)

        return redirect(url_for('main.search_results', query=query))

    return render_template('search.html', title = 'search Book', form=form)


@bp.route('/search/<query>', methods=['GET', 'POST'])
@login_required
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

    search_result = sorted(search_result.items(), key=lambda x: x[1], reverse=True)

    print(search_result)
    books = []
    for elem in search_result:
        books.append(elem[0])
        
    
    return render_template('search_results.html', books = books[:5])


@bp.route('/get/<book>', methods=['GET', 'POST'])
@login_required
def get(book):
    print(book)
    print(current_user)
    return render_template('get.html', book=book)


@bp.route('/home', methods=['GET', 'POST'])#might not need post
@login_required
def home(): 
    return render_template('home.html', title = 'Home Page')


@bp.route('/pickup', methods=['GET', 'POST'])
@login_required
def pickup():
    return render_template('pickup.html', title = "Pick Up")


@bp.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    return render_template('reserve.html', title="Reserve")

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = get_SearchForm()
