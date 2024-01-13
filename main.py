from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import datetime

from core.conf import fk_host, fk_port, fk_debug
from core.init import Inits
from view.adm.user_manage import user_manage
from view.adm.article_manage import article_manage
from view.adm.admin import admin
from view.adm.data import data
from api.private import private

app = Flask(__name__)
i = Inits()

# 前端请求跨域
CORS(app)

# 这个key要定义成变量
app.secret_key = 'ertyuiplbcvrtRTYssa345oplyt'
app.config['JWT_SECRET_KEY'] = 'errShare123321qawsedrftgyhnbvcAXFBJK'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)
app.config['JSON_AS_ASCII'] = False
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'
app.register_blueprint(user_manage)
app.register_blueprint(admin)
app.register_blueprint(article_manage)
app.register_blueprint(data)
app.register_blueprint(private)
jwt = JWTManager(app)


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
