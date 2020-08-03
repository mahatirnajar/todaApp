from todaApp.models import Project
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

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

