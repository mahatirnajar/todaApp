from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY']  = '5791628bb0b13ce0c676dfde280ba235'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

from todaApp import routes