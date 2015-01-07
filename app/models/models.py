from app import db
from flask.ext.security import RoleMixin, UserMixin
from sqlalchemy.sql.expression import func

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=func.now(), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    # flask security trackable fields
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String())
    current_login_ip = db.Column(db.String())
    login_count = db.Column(db.Integer())

    created_at = db.Column(db.DateTime(), default=func.now(), nullable=False)

    # relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return 'User{id:%s, email:%s}' % (self.id, self.email)

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, nullable=True)