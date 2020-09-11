import requests, json, urllib, random, string, ssl, os, logging, config, datetime, math
from flask import Flask, request
from flask_restful import Api, Resource
from config import Config
from logging.config import dictConfig
from logdna import LogDNAHandler

dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }
            },
            'handlers': {
                'logdna': {
                    'level': logging.DEBUG,
                    'class': 'logging.handlers.LogDNAHandler',
                    'key': os.environ.get('LOGDNA_APIKEY'),
                    'options': {
                        'app': 'utility-02cn.py',
                        'tags': os.environ.get('SERVERNAME'),
                        'env': os.environ.get('ENVIRONMENT'),
                        'url': os.environ.get('LOGDNA_LOGHOST'),
                        'index_meta': True,
                    },
                 },
            },
            'root': {
                'level': logging.DEBUG,
                'handlers': ['logdna']
            }
        })

HOST = '0.0.0.0'
PORT = 8110

app = Flask(__name__)
app.logger.info("Starting zero to cloud native utility")

app.config.from_object(Config)

api = Api(app)

def getiamtoken(apikey):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic Yng6Yng='
    }
    parms = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey", "apikey": apikey}

    try:
        resp = requests.post(app.config['IAM_ENDPOINT'] + "/identity/token?" + urllib.parse.urlencode(parms), headers=headers, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError as errc:
        quit()
    except requests.exceptions.Timeout as errt:
        quit()
    except requests.exceptions.HTTPError as errb:
        quit()
    iam = resp.json()
    return iam  


class GetIAMToken(Resource):
    def get(self):
        try:
            input_json_data = request.get_json()
            if "reqid" in input_json_data:
                reqid = input_json_data['reqid']
            else:
                reqid = ''
            app.logger.info("{} Starting Zero To Cloud Native Utility - request to get IAM Token.".format(reqid))
            
            apikey = input_json_data['apikey']
            try:
                iamtoken=getiamtoken(apikey)
            except:
                # Try twice in case API fails first time
                try:
                    iamtoken=getiamtoken(apikey)
                except Exception as e:
                    app.logger.error("{} Error Zero To Cloud Native Utility - Problem getting IAM Key {}".format(reqid, e))
                    return {
                        "Status":"Problem getting IAM Key for request"+reqid
                    }
            app.logger.info("{} Successfully got iam token".format(reqid))
            return {
                "Status":"Successfully got IAM Key for request"+reqid,
                "iamtoken": iamtoken
            }
        except Exception as e:
            app.logger.error("{} Error Cloudpak Provisioner Utility - Problem getting IAM Key {}".format(reqid, e))
            return {
                        "Status":"Problem getting IAM Key for request"+reqid
            }
        
api.add_resource(GetIAMToken, '/api/v1/getiamtoken/')

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, threaded=True, debug=False)