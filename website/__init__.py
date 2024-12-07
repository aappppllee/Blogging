from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
DB_NAME = "database.db"

print(f"Base Directory: {BASE_DIR}")


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, DB_NAME)}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment, Like

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    db_path = os.path.join(BASE_DIR, DB_NAME)
    print(f"Database Path: {db_path}")
    if not path.exists(db_path):
        # Ensure the parent directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with app.app_context():
            db.create_all()
        print("Created database!")
    else:
        print("Database already exists.")
