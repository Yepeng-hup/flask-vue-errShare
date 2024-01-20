from flask import Blueprint, jsonify, request
import traceback
import copy
import random
from flask_jwt_extended import jwt_required
from collections import Counter

from model.mongo.mgMode import Mg_mode
from core.httpStatus import Http_status
from core.utils.utils import check_network_status, check_localhost_site, check_server_status, \
    show_all_user_num
from core.conf import mg_host, mg_port, fk_host, fk_port, fk_ssl_type
from core.utils.utils import check_token
from core.svclog import svc_log_err

data = Blueprint("data", __name__)
mg = Mg_mode()


def poem_db() -> str:
    poem_list = [
        '一道残阳铺水中，半江瑟瑟半江红。',
        '春风桃李花开夜，秋雨梧桐叶落时。',
        '天生我材必有用，千金散尽还复来。',
        '古来圣贤皆寂寞，惟有饮者留其名。',
        '我寄愁心与明月，随君直到夜郎西。',
        '正是江南好风景，落花时节又逢君。',

    ]
    return random.choice(poem_list)

@data.route("/info/l")
@jwt_required()
@check_token
def show_login_info():
    poem = poem_db()
    try:
        user_num = show_all_user_num()
        login_info_list = mg.select_login_info()
        return jsonify(
            {
                "code": Http_status.http_status_ok,
                "login_info_list": login_info_list,
                "poem": poem,
                "user_num": user_num,
            }
        )
    except:
        print(traceback.format_exc())
        return jsonify(
            {
                "code": Http_status.http_status_server_err,
                "login_info_list": [],
                "poem": poem,
                "user_num": user_num,
            }
        )


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



