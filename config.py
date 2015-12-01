import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY='Do not try to guess'
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SUBJECT_PREFIX='[MIKE]'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER='smtp.qq.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_SENDER=os.environ.get('MAIL_ADMIN')
    MAIL_USERNAME=os.environ.get('MAIL_ADMIN')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    ADMIN=os.environ.get('MAIL_ADMIN')
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data-dev.sqlite')
class TestConfig(Config):
    Testing=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data_test.sqlite')
class ProductConfig(Config):
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'data_product.sqlite')

config={
'development':DevelopmentConfig,
'test':TestConfig,
'product':ProductConfig,
'default':DevelopmentConfig
}
