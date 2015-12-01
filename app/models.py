
from flask.ext.sqlalchemy import SQLAlchemy
from . import db
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    users=db.relationship('User',backref='role')
    def __repr__(self):
        return '<Role>{}</Role>'.format(self.name)
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    username=db.Column(db.String(64),unique=True,index=True)
    def __repr__(self):
        return '<Username>{}</Username>'.format(self.username)
