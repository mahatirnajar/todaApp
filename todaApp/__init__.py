from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from todaApp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view='users.login'

migrate = Migrate()

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from todaApp.users.routes import users
    from todaApp.tasks.routes import tasks
    from todaApp.main.routes import main
    from todaApp.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app