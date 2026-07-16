class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'talentbridge-secret-key-change-in-production'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        'mysql+mysqlconnector://root:@localhost/talent_bridge'
    )


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        'mysql+mysqlconnector://root:@localhost/talent_bridge'
    )