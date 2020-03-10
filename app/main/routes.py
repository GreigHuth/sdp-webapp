
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from sqlalchemy import or_
from app import db
from app.main.forms import  get_SearchForm
from app.models import User, Book
from app.main import bp


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


@bp.route('/get', methods=['GET','POST'])
@login_required
def get():

    form = get_SearchForm()
    if request.method == 'POST':  
        query = form.q.data
        print (query)

        return redirect(url_for('main.get_search', query=query))

    return render_template('get.html', title = 'Get Book', form=form)


@bp.route('/get/search/<query>', methods=['GET', 'POST'])
@login_required
def get_search(query):
     

    #search the database for book titles 
    search = "%{}%".format(query)

    #get all the books with titles similar to the statement
    books = db.session.query(Book).all()
    print (books)

    return render_template('get_search.html', books = books)


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
