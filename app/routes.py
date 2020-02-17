from flask import render_template, flash, redirect, url_for, request
from app import app, db
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.forms import LoginForm, SignupForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Landing Page')

@app.route('/login', methods=['GET', 'POST'])
def login():

    # dont need to log the user in if theyre already logged in
    if current_user.is_authenticated:
        #TODO change this to redirect to /home
        return redirect(url_for('index'))

    form = LoginForm()

    #returns true if request method is POST, GET if false
    # POST - Used when the page is submitting a form 
    # GET - used when just returning html files
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # if credentials are invalid then prompt for correct credentials
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or password')
            return redirect(url_for('login'))

        #this part actually does the user login
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")

        #this part returns the user to the page they tried to access if they tried to
        #   access a page that requires authentication
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index') #TODO this should redirect to /home
        return redirect(next_page) 
    
    return render_template('login.html', title ='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index')) #TODO this should redirect to /home

    form = SignupForm()
    #returns true if request method is POST, GET if false
    # POST - Used when the page is submitting a form 
    # GET - used when just returning html files
    if form.validate_on_submit():    
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user) # ignore these errors
        db.session.commit()
        flash('Successfully registered!')
        return redirect(url_for('login'))
    return render_template('signup.html', title = 'Sign up', form=form)