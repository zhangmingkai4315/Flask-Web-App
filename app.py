from flask import Flask,render_template
from flask import request
from flask import current_app
from flask import make_response,redirect,abort
# ///////////////////////////

from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap

# ///////////////////////////

print __name__
app=Flask(__name__)
@app.route('/')
def index():
    user_agent=request.headers.get('User-Agent')
    # return '<h1>Hello world ! </h1><h3>{}</h3><h4>{}</h4>'.format(user_agent,current_app.name)
    return render_template('index.html')
@app.route('/user/<name>')
def user(name):
    if name=='mingkai':
        # response=make_response('<h1> Hi %s</h1' % name)
        # response.set_cookie('user',name)
        # return response,200
        return render_template('user.html',name=name)
    elif name=='admin':
        # return redirect('/')
        return render_template('admin.html',name=name)
    else:
        abort(404)

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
if __name__ == '__main__':
    app.debug=True
    bootstrap=Bootstrap(app)
    manager=Manager(app)
    manager.run()
