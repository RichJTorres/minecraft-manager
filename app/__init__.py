from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore


app = Flask(__name__)
# app.config.from_object('app.config')
app.config.from_envvar('APPLICATION_SETTINGS')

db = SQLAlchemy(app)

import models


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)
jar_path = app.config['SERVER_JAR_PATH']

import views
db.drop_all()
db.create_all()
admin = models.User()
admin.email = app.config['ADMIN_DEFAULT_EMAIL']
admin.password = app.config['ADMIN_DEFAULT_PASSWORD']
admin.active = True
db.session.add(admin)
db.session.commit()

@app.context_processor
def context_process():
    from flask.ext.security import current_user
    return {current_user: current_user}
