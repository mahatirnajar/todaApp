# from todaApp import db
from todaApp.models import Project
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from todaApp.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class loginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class NewProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description', validators=[Length(min=2, max=200)])
    due_date =  DateField('Due Date')
    submit = SubmitField('Save')


class NewTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100)])
    description = StringField('Description', validators=[Length(min=2, max=200)])
    due_date =  DateField('Due Date', validators=[DataRequired()])
    project = SelectField('Project', coerce=int)
    submit = SubmitField('Save')
