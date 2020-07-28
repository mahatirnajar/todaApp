from datetime import datetime
from todaApp import  db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'"



class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300))
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    task = db.relationship('Task', backref='task', lazy=True)

    def __repr__(self):
        return f" Project('{self.title}')"

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300))
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    project = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __repr__(self):
        return f" Task('{self.title}')"

