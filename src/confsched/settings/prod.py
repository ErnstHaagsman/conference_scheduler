from .db import *

SECRET_KEY = os.environ['SECRET_KEY']

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

DEFAULT_FROM_EMAIL = 'noreply@confsched.ernsthaagsman.com'

ALLOWED_HOSTS = os.environ['HOSTS'].split(',')

DEBUG = False
