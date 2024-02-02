import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'avelovic96@gmail.com'
    MAIL_PASSWORD = 'cyka iffl xuba qsvk'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True