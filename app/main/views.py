from flask import render_template,session,url_for,flash
from flask import request
from flask import current_app
from flask import make_response,redirect,abort
from ..models import User
from .form import NameForm
from .. import db
from . import main


@main.route('/')
def index():
    user_agent=request.headers.get('User-Agent')
    # return '<h1>Hello world ! </h1><h3>{}</h3><h4>{}</h4>'.format(user_agent,current_app.name)
    print url_for('.index')
    return render_template('index.html')
@main.route('/login',methods=['GET','POST'])
def login():
    form=NameForm()
    if form.validate_on_submit():
        oldname=session.get('user')
        name=form.name.data
        if(oldname is not None and oldname!=name):
            flash('YOU HAVE CHANGED YOUR NAME FROM:{} TO {}'.format(oldname,name))
        session['user']=name
        return redirect(url_for('.login'))
        # name=form.name.data
        # form.name.data=''
    return render_template('login.html',form=form,name=session.get('user'))
@main.route('/user/<name>')
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
@main.route('/users')
def userlist():
    userlist=['mike','alice','bob']
    return render_template('users.html',users=userlist)
