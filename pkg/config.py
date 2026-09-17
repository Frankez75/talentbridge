import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        '7110-in-usage-filbar-88'
    )
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        'mysql+mysqlconnector://root:@localhost/talent_bridge'
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        'mysql+mysqlconnector://fnl:75ace75of75excel%23@mysql-fnl.alwaysdata.net/fnl_talentbridge_db'
    )