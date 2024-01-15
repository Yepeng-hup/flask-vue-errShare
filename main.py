from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import datetime

from core.conf import fk_host, fk_port, fk_debug, \
    fk_jwt_secret_key, \
    fk_jwt_token_expires_time, \
    fk_secret_key, \
    fk_timezone
from core.init import Inits
from view.adm.user_manage import user_manage
from view.adm.article_manage import article_manage
from view.adm.admin import admin
from view.adm.data import data

app = Flask(__name__)
i = Inits()
CORS(app)  # 前端请求跨域
app.secret_key = fk_secret_key
app.config['JWT_SECRET_KEY'] = fk_jwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=fk_jwt_token_expires_time)
app.config['JSON_AS_ASCII'] = False
app.config['SCHEDULER_TIMEZONE'] = fk_timezone
jwt = JWTManager(app)
app.register_blueprint(user_manage)
app.register_blueprint(admin)
app.register_blueprint(article_manage)
app.register_blueprint(data)


def clogo():
    print("====================================================================")
    print("==                                                                ==")
    print("==   Welcome to the errShare technology error sharing platform    ==")
    print("==  github: https://github.com/Yepeng-hup/flask-vue-errShare.git  ==")
    print("==                                                                ==")
    print("====================================================================")


if __name__ == "__main__":
    clogo()
    i.init_sqlite()
    i.init_user_and_role()
    app.run(debug=fk_debug, host=fk_host, port=fk_port)
