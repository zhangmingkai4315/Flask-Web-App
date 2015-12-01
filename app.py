from flask import Flask,render_template,session,url_for,flash
from flask import request
from flask import current_app
from flask import make_response,redirect,abort
from datetime import datetime
import os
from threading import Thread
# ///////////////////////////

from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
# //form class
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

from flask.ext.sqlalchemy import SQLAlchemy
basedir=os.path.abspath(os.path.dirname(__file__))


from flask.ext.migrate import Migrate,MigrateCommand
from flask.ext.mail import Mail,Message


# ///////////////////////////

app=Flask(__name__)
app.debug=True
app.config['SECRET_KEY']='Do not try to guess'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

app.config['SUBJECT_PREFIX']='[MIKE]'
app.config['MAIL_SENDER']=os.environ.get('MAIL_ADMIN')
app.config['MAIL_SERVER']='smtp.qq.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True

app.config['MAIL_USERNAME']=os.environ.get('MAIL_ADMIN')
app.config['MAIL_PASSWORD']=os.environ.get('MAIL_PASSWORD')
app.config['ADMIN']=os.environ.get('MAIL_ADMIN')

def send_mail(to,subject,template,**kwargs):
    msg=Message(app.config['SUBJECT_PREFIX']+subject,sender=app.config['MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)

    thread_mail=Thread(target=send_async_mail,args=[app,msg])
    thread_mail.start()
    return thread_mail



def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)


db=SQLAlchemy(app)
bootstrap=Bootstrap(app)
moment=Moment(app)
migrate=Migrate(app,db)
mail=Mail(app)




class NameForm(Form):
    name=StringField('What is your name?',validators=[Required()])
    submit=SubmitField('Submit')

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





@app.route('/')
def index():
    user_agent=request.headers.get('User-Agent')
    # return '<h1>Hello world ! </h1><h3>{}</h3><h4>{}</h4>'.format(user_agent,current_app.name)
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    form=NameForm()
    if form.validate_on_submit():
        oldname=session.get('user')
        name=form.name.data
        if(oldname is not None and oldname!=name):
            flash('YOU HAVE CHANGED YOUR NAME FROM:{} TO {}'.format(oldname,name))
        session['user']=name
        return redirect(url_for('login'))
        # name=form.name.data
        # form.name.data=''
    return render_template('login.html',form=form,name=session.get('user'))
@app.route('/user/<name>')
def user(name):
    user=User.query.filter_by(username=name).first()
    if user is None:
        return redirect('/')
    if user.role.name=='admin':
        if app.config['ADMIN']:
            send_mail(app.config['ADMIN'],'admin login','mail/login',user=user)
        return render_template('admin.html',name=name)
    elif user.role.name=='user':
        return render_template('user.html',name=name,current_time=datetime.utcnow())
    else:
        return redirect('/')
    # if name=='mingkai':
    #     # response=make_response('<h1> Hi %s</h1' % name)
    #     # response.set_cookie('user',name)
    #     # return response,200
    #     return render_template('user.html',name=name,current_time=datetime.utcnow())
    # elif name=='admin':
    #     # return redirect('/')
    #     return render_template('admin.html',name=name)
    # else:
    #     abort(404)
@app.route('/users')
def userlist():
    userlist=['mike','alice','bob']
    return render_template('users.html',users=userlist)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500

# //////////////






# ////////////////

if __name__ == '__main__':

    manager=Manager(app)
    manager.add_command('db',MigrateCommand)
    manager.run()
