from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import datetime

from core.conf import fk_host, fk_port, fk_debug, \
    fk_jwt_secret_key, \
    fk_jwt_token_expires_time, \
    fk_secret_key, \
    fk_timezone, \
    fk_file_video_acc_white
from core.init import Inits
from core.svclog import svc_log_warn
from view.adm.user_manage import user_manage
from view.adm.article_manage import article_manage
from view.adm.admin import admin
from view.adm.data import data
from view.adm.systems import systems
from view.adm.iptabless import iptabless
from view.adm.black import black

app = Flask(__name__)
i = Inits()
IMG_FOLDER = 'upload/images'
VIDEO_FOLDER = 'upload/video'
CORS(app)
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
app.register_blueprint(systems)
app.register_blueprint(iptabless)
app.register_blueprint(black)


def clogo():
    print("====================================================================")
    print("==                                                                ==")
    print("==   Welcome to the errShare technology error sharing platform    ==")
    print("==  github: https://github.com/Yepeng-hup/flask-vue-errShare.git  ==")
    print("==                                                                ==")
    print("====================================================================")


# 获取所有路由,可以根据这个细分权限，启动时可以直接初始化掉，我这里面没有细分权限，只是编写了这个
def get_all_route() -> list:
    route_list = list()
    for rule in app.url_map.iter_rules():
        route_obj = {
            "route_name": rule.endpoint,
            "route_path": rule.rule,
        }
        route_list.append(route_obj)
    print(route_list)
    return route_list


@app.route('/files/<path:filename>')
def protected_file(filename):
    # client_ip = request.remote_addr
    # if len(fk_file_video_acc_white) == 1:
    #     if fk_file_video_acc_white[0] == "all":
    #         return send_from_directory(IMG_FOLDER, filename)
    # if client_ip in fk_file_video_acc_white:
        return send_from_directory(IMG_FOLDER, filename)
    # else:
    #     svc_log_warn(f"error you don't have permission images -> [{client_ip}]")
    #     return jsonify({"code": 404, "msg": "There is no such thing"})


@app.route('/videos/<path:filename>')
def protected_video(filename):
    client_ip = request.remote_addr
    if len(fk_file_video_acc_white) == 1:
        if fk_file_video_acc_white[0] == "all":
            return send_from_directory(VIDEO_FOLDER, filename)
    if client_ip in fk_file_video_acc_white:
        return send_from_directory(VIDEO_FOLDER, filename)
    else:
        svc_log_warn(f"error you don't have permission video -> [{client_ip}]")
        return jsonify({"code": 404, "msg": "There is no such thing"})


if __name__ == "__main__":
    clogo()
    i.init_sqlite()
    i.init_user_and_role()
    app.run(debug=fk_debug, host=fk_host, port=fk_port)
