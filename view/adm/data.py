from flask import Blueprint, jsonify, request
import traceback

from model.mongo.mgMode import Mg_mode
from core.httpStatus import Http_status
from core.utils.utils import check_network_status, check_localhost_site, check_server_status
from core.conf import mg_host, mg_port, fk_host, fk_port, fk_ssl_type
from core.svclog import svc_log_err


data = Blueprint("data", __name__)
mg = Mg_mode()


@data.route("/info/l")
def show_login_info():
    try:
        login_info_list = mg.select_login_info()
        return jsonify({"code": Http_status.http_status_ok, "login_info_list": login_info_list})
    except:
        print(traceback.format_exc())
        return jsonify({"code": Http_status.http_status_server_err, "login_info_list": []})


@data.route("/check", methods=['POST'])
def check_all():
    data = request.get_json()
    action = data.get('action')
    if action == "mongoCheck":
        # 检测逻辑
        if not check_network_status(mg_host, mg_port):
            return jsonify({
                "code": Http_status.http_status_server_err,
                "msg": "mongo stop ..."
            })
        return jsonify({
            "code": Http_status.http_status_ok,
            "msg": "mongo running ..."
        })

    elif action == "serverCheck":
        status = check_server_status()
        return jsonify({"code": Http_status.http_status_ok, "msg": status})
    elif action == "siteCheck":
        url = fk_ssl_type+"://"+str(fk_host)+":"+str(fk_port)+"/index"
        if check_localhost_site(url):
            return jsonify({"code": Http_status.http_status_ok, "msg": "errShare site running ..."})
        else:
            return jsonify({"code": Http_status.http_status_server_err, "msg": "errShare site noResponse ..."})
    else:
        svc_log_err(f"not is the action [{action}]")
        return


@data.route("/pic")
def show_all_picture():

    pass
