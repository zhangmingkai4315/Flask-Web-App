from flask import Flask
from flask import request
from flask import current_app
from flask import make_response,redirect,abort
# ///////////////////////////

from flask.ext.script import Manager

# ///////////////////////////

print __name__
app=Flask(__name__)
@app.route('/')
def index():
    user_agent=request.headers.get('User-Agent')
    return '<h1>Hello world ! </h1><h3>{}</h3><h4>{}</h4>'.format(user_agent,current_app.name)

@app.route('/user/<name>')
def user(name):
    if name=='mingkai':
        response=make_response('<h1> Hi %s</h1' % name)
        response.set_cookie('user',name)
        return response,200
    elif name=='admin':
        return redirect('/')
    else:
        abort(404)


if __name__ == '__main__':
    app.debug=True
    manager=Manager(app)
    manager.run()
