import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from flask_mail import Mail
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
oauth = OAuth()

def create_app():
    from pkg import config
    from pkg.models import db

    app = Flask(__name__, instance_relative_config=True)

    # Load config
    app.config.from_pyfile('config.py', silent=True)
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(config.ProductionConfig)
    else:
        app.config.from_object(config.DevelopmentConfig)
        
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    oauth.init_app(app)

    # Register Google OAuth provider
    oauth.register(
        name='google',
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Register blueprints
    from pkg.auth_routes import auth
    from pkg.user_routes import user
    from pkg.admin_routes import admin
    from pkg.transaction_routes import transaction
    from pkg.main_routes import main
    from pkg.social_routes import social

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        from flask import render_template
        return render_template('errors/500.html'), 500

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(transaction)
    app.register_blueprint(social)

    return app