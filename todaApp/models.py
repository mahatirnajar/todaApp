from datetime import datetime
from todaApp import  db

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

