from flask_security import SQLAlchemyUserDatastore
from .models import db,User,Role

datastore  = SQLAlchemyUserDatastore(db,User,Role)     # Bridging Flask-Security and SQLAlchemy