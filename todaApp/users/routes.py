import os
from flask import render_template, request, redirect, url_for, abort, Blueprint, current_app
from todaApp import db, bcrypt
from todaApp.models import Project, User
from todaApp.users.forms import (RegistrationForm, loginForm,  UpdateAccountForm,
                                RequestResetForm, ResetPasswordForm)
from flask_login import login_user, current_user, logout_user, login_required
from todaApp.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    form= RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))

    return render_template('login.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data :
            
            try :
                current_picture = os.path.join(current_app.root_path, 'static/img/profile_pict', current_user.image_file)
                os.remove(current_picture)
            except:
                pass
            
            picture_file= save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data =  current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='img/profile_pict/'+current_user.image_file)

    projects = Project.query.filter_by(user=current_user.id).all()
    return render_template('account.html', image_file=image_file, form=form, projects=projects)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        print('masuk')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)