from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

import models


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)
jar_path = app.config['SERVER_JAR_PATH']

import views

db.create_all()
admin = models.User()
admin.email = app.config['DEFAULT_ADMIN_EMAIL']
admin.password = app.config['DEFAULT_ADMIN_PASSWORD']
admin.active = True
db.session.add(admin)
db.session.commit()

@app.context_processor
def context_process():
    from flask.ext.security import current_user
    return {current_user: current_user}
