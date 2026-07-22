from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    from pkg import config
    from pkg.models import db

    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_object(config.DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from pkg.auth_routes import auth
    from pkg.user_routes import user
    from pkg.admin_routes import admin
    from pkg.transaction_routes import transaction
    from pkg.main_routes import main

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(transaction)

    return app