import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    ENVIRONMENT = os.environ.get('ENVIRONMENT')
    LOGDNA_APIKEY = os.environ.get('LOGDNA_APIKEY')
    LOGDNA_LOGHOST = os.environ.get('LOGDNA_LOGHOST')
    SERVERNAME = os.environ.get('SERVERNAME')
    IAM_ENDPOINT = os.environ.get("IAM_ENDPOINT")
