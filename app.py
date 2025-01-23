from flask import Flask
from flask_security import  Security
from application.models import db
from application.config import Config
from application.datastore import datastore
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.security = Security(app, datastore)

with app.app_context():
    import application.views

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='admin',description='Admin role')
    datastore.find_or_create_role(name='user',description='User role')
    db.session.commit()

    if not datastore.find_user(email='admin@email.com'):
        datastore.create_user(email='admin@email.com',password=generate_password_hash('admin'),name='admin',roles=['admin'])
    
    db.session.commit()

if(__name__=='__main__'):
    app.run(debug=True)