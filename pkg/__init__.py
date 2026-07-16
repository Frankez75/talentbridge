from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app():
    from pkg import config
    from pkg.models import db

    app = Flask(__name__, instance_relative_config=True)

    # Load config from instance/config.py first, then pkg/config.py class
    app.config.from_pyfile('config.py', silent=True)
    app.config.from_object(config.DevelopmentConfig)

    db.init_app(app)
    csrf.init_app(app)

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