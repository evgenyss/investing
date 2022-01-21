from webapp.db import db
from webapp import create_app

db.create_all(app=create_app())
