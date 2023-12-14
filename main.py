from flask import Flask

from core.conf import fk_host, fk_port, fk_debug
from model.sqlite.create import create_tables
from view.front.test import test
from view.front.user import user

app = Flask(__name__)
app.secret_key = 'ertyuiplbcvrtRTYssa345oplyt'
app.config['JSON_AS_ASCII'] = False
app.config['SCHEDULER_TIMEZONE'] = 'Asia/Shanghai'
app.register_blueprint(test)
app.register_blueprint(user)


def clogo():
    print("===========================================================")
    print("==                                                       ==")
    print("==            欢迎使用errShare技术错误分享平台                ==")
    print("==  github: https://github.com/Yepeng-hup/errShare.git   ==")
    print("==                                                       ==")
    print("===========================================================")

if __name__ == "__main__":
    # create_tables()
    # p.encryption("123456")
    # p.decrypt("sha256:260000$LJ8V42ju0n06eawy$8fc4432e5547e08e765778c60988189cc683c47c4ccac452f2829814a1e2cf52", "123456")
    clogo()
    app.run(debug=False, host=fk_host, port=fk_port)
