from flask import render_template, request, redirect, url_for, abort
from todaApp import app, db
from todaApp.models import Task, Project
from todaApp.forms import NewProjectForm, NewTaskForm


@app.route("/")
def home():
    tasks = Task.query.all()
    projects = Project.query.all()
    return render_template('home.html', tasks=tasks, projects=projects)

@app.route("/project/new", methods=['GET', 'POST'])
def newProject():
    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project(
            title = form.title.data,
            description = form.description.data,
            due_date = form.due_date.data
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new-project.html', form=form,  legend='New Project')

@app.route("/project/update/<int:project_id>", methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    return render_template('new-project.html', form=form,  legend='Update Project')


@app.route("/project/delete/<int:project_id>", methods=['GET', 'POST'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/task/new", methods=['GET', 'POST'])
def newTask():
    form = NewTaskForm()
    form.project.choices = [(p.id, p.title) for p in Project.query.all()] 
    if form.validate_on_submit():
        tasks=Task(
            title=form.title.data,
            description=form.description.data,
            project=form.project.data,
            due_date=form.due_date.data            
        )
        db.session.add(tasks)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new-task.html', form=form, legend='New Task')


@app.route("/task/update/<int:todo_id>", methods=['GET', 'POST'])
def update_task(todo_id):
    task = Task.query.get_or_404(todo_id)
    form = NewTaskForm()
    form.project.choices = [(p.id, p.title) for p in Project.query.all()]
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
        return redirect(url_for('home'))
    return render_template('new-task.html', form=form,  legend='Update task')


@app.route("/task/delete/<int:todo_id>", methods=['GET', 'POST'])
def delete_task(todo_id):
    task = Task.query.get_or_404(todo_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html')