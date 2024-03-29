from flask import Blueprint, jsonify, request
import traceback
from flask_jwt_extended import jwt_required
import re

from core.svclog import svc_log_info, svc_log_err
from core.httpStatus import Http_status
from model.sqlite.sqlite import cursor
from model.sqlite.select import Select_tables
from core.utils.utils import check_token, delete_lines


black = Blueprint("black", __name__)
s = Select_tables()


@black.route("/black/cfg", methods=['POST'])
@jwt_required()
@check_token
def black_ip_cfg():
    data = request.get_json()
    service_name = data.get('serviceName')
    ip = data.get('ip')
    black_type = data.get('type')
    if len(black_type) != 1 or ip == '':
        return jsonify({
            "code": Http_status.http_status_server_err,
            "msg": "表单错误"
        })
    if black_type[0] == "deny":
        w_init = service_name+":"+ip+":deny"
        try:
            with open('/etc/hosts.deny', 'a') as file:
                file.write(w_init+"\n")
            return jsonify({
                "code": Http_status.http_status_ok,
                "msg": "加入成功"
            })
        except:
            print(traceback.format_exc())
            svc_log_err(f"add type [deny] black list fail -> [{w_init}]")
            return jsonify({
                "code": Http_status.http_status_server_err,
                "msg": "加入失败"
            })
    elif black_type[0] == "local":
        try:
            cursor.execute("INSERT INTO blacklist (ipaddr) VALUES (?)", (ip,))
            return jsonify({
                "code": Http_status.http_status_ok,
                "msg": "加入成功"
            })
        except:
            print(traceback.format_exc())
            svc_log_err(f"add type [local] black list fail -> [{ip}]")
            return jsonify({
                "code": Http_status.http_status_server_err,
                "msg": "加入失败"
            })
    else:
        return jsonify({
            "code": Http_status.http_status_server_err,
            "msg": "没有这种类型"
        })


@black.route("/black/show", methods=['POST'])
@jwt_required()
@check_token
def show_black():
    local_list = []
    data = request.get_json()
    title_name = data.get('name')
    if title_name == "local":
        try:
            rel = s.show_select_rel("SELECT ipaddr  FROM blacklist")
            for i in rel:
                u = {
                    "address": i[0]
                }
                local_list.append(u)
            return jsonify({"code": Http_status.http_status_ok, "msg": "获取local成功", "s_name": "local", "local_data": local_list})
        except:
            print(traceback.format_exc())
            svc_log_err("show [local] type black list fail")
            return jsonify({"code": Http_status.http_status_server_err, "msg": "获取local失败"})
    else:
        deny_list = []
        pattern = r'^#.*$'
        try:
            with open("/etc/hosts.deny", "r") as file:
                for i in file:
                    if not re.match(pattern, i):
                        u = {
                            "ruleStr": i
                        }
                        deny_list.append(u)
            return jsonify({"code": Http_status.http_status_ok, "msg": "获取deny成功", "s_name": "deny", "deny_data": deny_list, })
        except:
            print(traceback.format_exc())
            svc_log_err("show [deny] type black list fail")
            return jsonify({"code": Http_status.http_status_server_err, "msg": "获取deny失败"})


@black.route("/black/local/del", methods=['DELETE'])
@jwt_required()
@check_token
def delete_local():
    data = request.get_json()
    del_ip = data.get('ip')
    try:
        cursor.execute("DELETE FROM blacklist WHERE ipaddr=?", (del_ip,))
        return jsonify({"code": Http_status.http_status_ok, "msg": "删除成功"})
    except:
        print(traceback.format_exc())
        return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败"})


@black.route("/black/deny/del", methods=['DELETE'])
@jwt_required()
@check_token
def delete_deny():
    data = request.get_json()
    deny_rule = data.get('denyRule')
    if delete_lines("/etc/hosts.deny", deny_rule):
        return jsonify({"code": Http_status.http_status_ok, "msg": "删除成功"})
    return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败"})


