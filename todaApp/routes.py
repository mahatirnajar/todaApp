import os
import secrets
from PIL import Image
from flask import render_template, request, redirect, url_for, abort
from todaApp import app, db, bcrypt
from todaApp.models import Task, Project, User
from todaApp.forms import NewProjectForm, NewTaskForm, RegistrationForm, loginForm, UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/register", methods=['GET', 'POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))


@app.route("/")
@login_required
def home():
    tasks = Task.query.all()
    projects = Project.query.all()
    return render_template('home.html', tasks=tasks, projects=projects)


@app.route("/project/new", methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('home'))
    return render_template('new-project.html', form=form,  legend='Update Project')


@app.route("/project/delete/<int:project_id>", methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/task/new", methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def delete_task(todo_id):
    task = Task.query.get_or_404(todo_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/about")
def about():
    return render_template('about.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile_pict', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data :
            current_picture = os.path.join(app.root_path, 'static/img/profile_pict', current_user.image_file)
            os.remove(current_picture)
            picture_file= save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data =  current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='img/profile_pict/'+current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)