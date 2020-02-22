from flask import render_template, flash, redirect, url_for, request
import paramiko
from app import app, db, ssh_client
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Book
from app.forms import LoginForm, SignupForm


@app.route('/')
@app.route('/index')

def index():
  

    return render_template('index.html', title='Landing Page')

@app.route('/login', methods=['GET', 'POST'])
def login():

    # dont need to log the user in if theyre already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    #returns true if request method is POST, GET if false
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        # if credentials are invalid then prompt for correct credentials
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or password')
            return redirect(url_for('login'))

        #actually does the user login
        login_user(user, remember=form.remember_me.data)
        

        #returns the user to the page they tried to access if they tried to
        #   access a page that requires authentication
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home') 
        return redirect(next_page) 
    
    return render_template('login.html', title ='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home')) #TODO this should redirect to /home

    form = SignupForm()

    #returns true if request method is POST, GET if false
    if form.validate_on_submit():    
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user) # ignore these errors
        db.session.commit()
        flash('Successfully registered!')
        return redirect(url_for('login'))
    return render_template('signup.html', title = 'Sign up', form=form)

#code for second demo remove before 3rd demo
@app.route('/demo', methods=['GET','POST'])
@login_required
def demo2():

    

    #gets book names 
    books = db.session.query(Book.name).all()
    books = [book[0] for book in books]

    if request.method == "POST":
        #connect to BB with ssh, plan to use sockets or something better in the future
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname='pichu', username='pi', password='turtlebot')

        #container for demo script
        demo_script = ""

        if   'grab' in request.form:
            flash("Grabbing demo running...")

            demo_script = "path/to/grabbing/script"
            
            
        
        elif 'nav' in request.form:
            flash("Navigation demo running...")

            demo_script = "path/to/nav/script"
            
            

        elif 'id' in request.form:
            flash("Identification demo running...")

            book_chosen = request.form["book"]
            demo_script = "path/to/id/script"
            
            
        stdin,stdout,stderr=ssh_client.exec_command(demo_script)

        return render_template('demo2.html', title = 'demo 2', books=books)
    
    #if not POST then just return the page
    else:
        return render_template('demo2.html', title = 'demo 2', books=books)


@app.route('/home', methods=['GET', 'POST'])#might not need post
@login_required
def home(): 
    return render_template('home.html', title = 'Home Page')

#TODO all of this
@app.route('/get', methods=['GET', 'POST'])
@login_required
def get():
    return render_template('pickup.html', title = "Get Book")


@app.route('/pickup', methods=['GET', 'POST'])
@login_required
def pickup():
    return render_template('pickup.html', title = "Pick Up")


@app.route('/reserve', methods=['GET', 'POST'])
@login_required
def reserve():
    return render_template('reserve.html', title="Reserve")