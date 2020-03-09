from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Optional
from app.models import User



#form for the get page
class get_SearchForm(FlaskForm):
    #ignore these errors if they show up
    searchTitle = StringField('Search for a specfic book.', validators=[Optional()])
    searchAuthor = StringField('Search for a specific author.', validators=[Optional()])
    searchGenre = StringField('Search for a specific genre.', validators=[Optional()])

    submit = SubmitField('Search')