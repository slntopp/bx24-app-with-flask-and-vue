import os

class Config(object):
	DEBUG = True
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4'.format(**os.environ)
	SECRET_KEY = os.urandom(24)
	CSRF_ENABLED = False
