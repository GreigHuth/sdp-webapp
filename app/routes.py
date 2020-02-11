from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm


@app.route('/')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #returns true if request method is POST, GET if false
    if form.validate_on_submit():
        flash('Login Requested for user {}, remember_me{}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    
    return render_template('login.html', title ='Sign In', form=form)