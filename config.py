import os

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or 'environment variable is set to an empty string'