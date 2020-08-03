from flask import render_template, request, redirect, url_for, abort, Blueprint
from todaApp import db
from todaApp.models import Task, Project, User
from todaApp.tasks.forms import NewProjectForm, NewTaskForm
from flask_login import current_user, login_required


tasks = Blueprint('tasks', __name__)


@tasks.route("/project/new", methods=['GET', 'POST'])
@login_required
def newProject():
    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project(
            title = form.title.data,
            description = form.description.data,
            due_date = form.due_date.data,
            user=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('main.home'))
    projects = Project.query.filter_by(user=current_user.id).all()
    return render_template('new-project.html', form=form,  legend='New Project', projects=projects)

@tasks.route("/project/update/<int:project_id>", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = NewProjectForm()
    if request.method =='GET':
        form.title.data = project.title
        form.description.data = project.description
        form.due_date.data = project.due_date
    elif form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.due_date = form.due_date.data
        db.session.commit()
        return redirect(url_for('tasks.single_project', project_id=project_id))
    projects = Project.query.filter_by(user=current_user.id).all()
    return render_template('new-project.html', form=form,  legend='Update Project', projects=projects)


@tasks.route("/project/delete/<int:project_id>", methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    task = Task.query.filter_by(project=project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('main.home'))


@tasks.route("/project/single/<int:project_id>", methods=['GET', 'POST'])
@login_required
def single_project(project_id):
    tasks= Task.query.filter_by(completed=False, project=project_id, user=current_user.id).order_by(Task.due_date).all()
    tasks_complete = Task.query.filter_by(completed=True, project=project_id, user=current_user.id).order_by(Task.due_date).all()
    project = Project.query.get_or_404(project_id)
    projects = Project.query.filter_by(user=current_user.id).all()
    return render_template('project.html', projects=projects, tasks=tasks, 
                            project=project, tasks_complete=tasks_complete)


@tasks.route("/task/new", methods=['GET', 'POST'])
@login_required
def newTask():
    form = NewTaskForm()
    form.project.choices = [(p.id, p.title) for p in Project.query.filter_by(user=current_user.id).all()] 
    if form.validate_on_submit():
        tasks=Task(
            title=form.title.data,
            description=form.description.data,
            project=form.project.data,
            due_date=form.due_date.data,
            user=current_user.id            
        )
        db.session.add(tasks)
        db.session.commit()
        return redirect(url_for('main.home'))
    projects = Project.query.filter_by(user=current_user.id).all()
    return render_template('new-task.html', form=form, legend='New Task', projects=projects)


@tasks.route("/task/update/<int:todo_id>", methods=['GET', 'POST'])
@login_required
def update_task(todo_id):
    task = Task.query.get_or_404(todo_id)
    form = NewTaskForm()
    form.project.choices = [(p.id, p.title) for p in Project.query.filter_by(user=current_user.id).all()]
    if request.method =='GET':
        form.title.data = task.title
        form.description.data = task.description
        form.project.data = task.project
        form.due_date.data = task.due_date
    elif form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.project = form.project.data
        task.due_date = form.due_date.data
        db.session.commit()
        return redirect(url_for('main.home'))
    projects = Project.query.filter_by(user=current_user.id).all()
    return render_template('new-task.html', form=form,  legend='Update task', projects=projects)

@tasks.route("/task/complete/<int:todo_id>", methods=['GET', 'POST'])
@login_required
def complete_task(todo_id):
    task = Task.query.get_or_404(todo_id)
    task.completed = not (task.completed)
    db.session.commit()
    return redirect(url_for('main.home'))



@tasks.route("/task/delete/<int:todo_id>", methods=['GET', 'POST'])
@login_required
def delete_task(todo_id):
    task = Task.query.get_or_404(todo_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.home'))