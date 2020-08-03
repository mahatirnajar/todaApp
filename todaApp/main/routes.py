from flask import render_template, Blueprint 
from todaApp.models import Task, Project, User
from flask_login import current_user, login_required


main = Blueprint('main', __name__)

@main.route("/")
@login_required
def home():
    tasks= Task.query.filter_by(completed=False, user=current_user.id).order_by(Task.due_date).all()
    tasks_complete = Task.query.filter_by(completed=True, user=current_user.id).order_by(Task.due_date).all()
    projects = Project.query.filter_by(user=current_user.id).all()
    return render_template('home.html', tasks=tasks, projects=projects, tasks_complete=tasks_complete)
