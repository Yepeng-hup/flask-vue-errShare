from flask import Blueprint, jsonify, request
import traceback
import copy
from flask_jwt_extended import jwt_required
from collections import Counter

from model.mongo.mgMode import Mg_mode
from core.httpStatus import Http_status
from core.utils.utils import check_network_status, check_localhost_site, check_server_status
from core.conf import mg_host, mg_port, fk_host, fk_port, fk_ssl_type
from core.utils.utils import check_token
from core.svclog import svc_log_err

data = Blueprint("data", __name__)
mg = Mg_mode()


@data.route("/info/l")
@jwt_required()
@check_token
def show_login_info():
    try:
        login_info_list = mg.select_login_info()
        return jsonify({"code": Http_status.http_status_ok, "login_info_list": login_info_list})
    except:
        print(traceback.format_exc())
        return jsonify({"code": Http_status.http_status_server_err, "login_info_list": []})


@data.route("/check", methods=['POST'])
@jwt_required()
@check_token
def check_all():
    data = request.get_json()
    action = data.get('action')
    if action == "mongoCheck":
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
        url = fk_ssl_type + "://" + str(fk_host) + ":" + str(fk_port) + "/index"
        if check_localhost_site(url):
            return jsonify({"code": Http_status.http_status_ok, "msg": "errShare site running ..."})
        else:
            return jsonify({"code": Http_status.http_status_server_err, "msg": "errShare site noResponse ..."})
    else:
        svc_log_err(f"not is the action [{action}]")
        return


@data.route("/pic/data")
@jwt_required()
@check_token
def show_all_picture():
    rel = mg.select_all_class({'_id': 0, 'date': 0, })
    deep_copy_rel_list = copy.deepcopy(rel)
    for c in rel:
        class_num = mg.select_wz_num({"class": c['class']})
        for d in deep_copy_rel_list:
            if c['class'] == d['class']:
                d.update({'num': class_num})
                break

    num_list = [d["num"] for d in deep_copy_rel_list]
    class_list = [d["class"] for d in deep_copy_rel_list]
    return jsonify({"code": Http_status.http_status_ok, "num_list": num_list, "class_list": class_list})


@data.route("/user/data/pic")
@jwt_required()
@check_token
def show_user_login_pic():
    login_username_list = mg.select_login_user({}, {'_id': 0, 'date': 0, })
    name_counts = Counter(login_username_list)
    username_num_list = list(name_counts.values())
    username_list = list(name_counts.keys())
    return jsonify({"code": Http_status.http_status_ok, "username_num_list": username_num_list, "username_list": username_list, })


