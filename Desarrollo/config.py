import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Cl@ve'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/myDB.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_PATH = 'app/uploads'
    UPLOAD_EXTENSIONS = ['.jpg', '.png', '.gif']
    MAX_CONTENT_LENGTH = 1024 * 1024