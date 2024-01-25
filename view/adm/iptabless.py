from flask import Blueprint, jsonify, request
import traceback
from flask_jwt_extended import jwt_required

from core.svclog import svc_log_info, svc_log_err
from core.utils.utils import check_token, run_linux_code
from core.httpStatus import Http_status
from model.secure.search import Search_secure
from core.conf import fk_search_not_str


iptabless = Blueprint("iptabless", __name__)
s = Search_secure()


@iptabless.route("/sys/iptables/cfg", methods=['POST'])
@jwt_required()
@check_token
def config_iptables():
    data = request.get_json()
    iptables_rule = data.get("rule")
    if "iptables" not in iptables_rule:
        return jsonify({"code": Http_status.http_status_server_err, "msg": "规则无效"})
    if not s.check_search_text(fk_search_not_str, iptables_rule):
        cmd = iptables_rule
        if run_linux_code(cmd) and run_linux_code("bash shell/iptables.sh save"):
            return jsonify({"code": Http_status.http_status_ok, "msg": "添加规则成功"})
        return jsonify({"code": Http_status.http_status_server_err, "msg": "添加规则失败"})
    else:
        return jsonify({"code": Http_status.http_status_server_err, "msg": "规则无效"})


@iptabless.route("/sys/iptables/select")
@jwt_required()
@check_token
def select_iptables_cfg():
    rule_list = []
    rule = []
    cmd = "bash shell/iptables.sh show"
    if not run_linux_code(cmd):
        svc_log_err(f"cmd run fail -> [{cmd}]")
        return jsonify({"code": Http_status.http_status_server_err, "msg": "获取规则失败"})
    try:
        with open('rule.txt', 'r') as file:
            for line in file:
                rule_list.append(line)
    except:
        print(traceback.format_exc())
        return jsonify({"code": Http_status.http_status_server_err, "msg": "获取规则失败"})
    for i in rule_list:
        # 拿到以中间空格为分割符
        parts = i.split(' ', 1)
        r = {
            "num": parts[0],
            "rule": parts[1],
        }
        rule.append(r)
    del rule_list

    response_obj = {
        "code": Http_status.http_status_ok,
        "rule_list": rule,
    }
    return jsonify(response_obj)


@iptabless.route("/sys/iptables/del", methods=['DELETE'])
@jwt_required()
@check_token
def del_iptables_cfg():
    data = request.get_json()
    rule_num = data.get('ruleNum')
    cmd = "iptables -D INPUT "+rule_num
    if run_linux_code(cmd) and run_linux_code("bash shell/iptables.sh save"):
        svc_log_info(f"use [{cmd}] ok")
        return jsonify({"code": Http_status.http_status_ok, "msg": "删除成功"})
    return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败"})
