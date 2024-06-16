import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '871ff536c5953c573b67296eeb2e22d16e76d43f433a66223ae88225a68947f8'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://postgres:54321@db:5432/postgres'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'jpg', 'png'}