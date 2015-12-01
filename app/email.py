from flask.ext.mail import Mail,Message
from threading import Thread

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
