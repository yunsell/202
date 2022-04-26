from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from routes.sda import Sda



app = Flask(__name__)
api = Api(app, version='1.0', title='SDA RESTApi')

# CORS 문제로 인해 모든 주소 허용 => 후에 수정필요
CORS(app)

# ADMINS EMAIL
ADMINS = ['jnn6576@dsong.co.kr']

# POST /sda/gen
api.add_namespace(Sda, '/sda') # SDA API


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler('127.0.0.1',
                               'jnn6576@dsong.co.kr',
                               ADMINS, 'Flask API Server 에러가 발생하였습니다.')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3030)


