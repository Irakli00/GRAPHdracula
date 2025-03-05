from os import path

class Config:
    BASE_DIRECTORY = path.abspath(path.dirname(__file__))
    SECRET_KEY = "DJSKJFSVSKEJB"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(BASE_DIRECTORY, "database.db")
    UPLOAD_PATH = path.join(BASE_DIRECTORY, "static", "upload")