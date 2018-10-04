import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'B0l04[1\n8w]fEzWp1Rd/eRG{qbVlO3A4yTsrrBa8kZAi7=BDdJ}i21'
    TOKEN_VALIDITY = 48  # hours
    SALT_LENGTH = 12  # value should be between 1 and 128
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    username = os.environ.get('MYSQL_USERNAME')
    password = os.environ.get('MYSQL_PASSWORD')
    hostname = os.environ.get('MYSQL_HOSTNAME')
    port = os.environ.get('MYSQL_PORT')
    database = os.environ.get('MYSQL_DATABASE')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}?charset=utf8mb4'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:root@localhost:9999/web-template?charset=utf8mb4'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
