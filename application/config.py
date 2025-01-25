import json
with open('./secrets.json') as f:
    secrets = json.load(f)
class Config:
    DEBUG = secrets["DEBUG"]
    SQLALCHEMY_DATABASE_URI =secrets["SQL_URI_SQLITE"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_HEADER_NAME = 'Authentication-Token'
    JWT_SECRET_KEY=secrets["JWT_SECRET_KEY"]