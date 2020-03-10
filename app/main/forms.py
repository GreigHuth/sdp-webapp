from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length, Optional
from app.models import User


#form for the get page
class get_SearchForm(FlaskForm):
    q = StringField(('Search for books by title, author or genre'), validators=[Optional()])
    submit = SubmitField('')
