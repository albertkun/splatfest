import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	HOST = 'database_host'
	DATABASE = 'DB'
	USERNAME = 'DB USER'
	SECRET_KEY = 'KEY'
	PORT = '5432'
	SSL_DISABLE = False

@staticmethod
def init_app(app):
	pass

@classmethod
def init_app(app):
	Config.init_app(app)

config = {

}
