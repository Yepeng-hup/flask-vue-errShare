from flask import Blueprint, jsonify, request
import traceback
from flask_jwt_extended import jwt_required

from model.sqlite.sqlite import cursor
from model.sqlite.select import Select_tables
from core.utils.utils import data_init, check_token, create_token
from core.httpStatus import Http_status
from model.secure.pwd import Pwd_encryption_decrypt
from core.svclog import svc_log_info, svc_log_err
from model.mongo.mgMode import Mg_mode

user_manage = Blueprint("user_manage", __name__)
s = Select_tables()
p = Pwd_encryption_decrypt()
mg = Mg_mode()


@user_manage.route("/err/login", methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('username')
    password = data.get('password')
    cursor.execute("SELECT username,password,role  FROM users WHERE username=?", (user_name,))
    rel = cursor.fetchall()
    if len(rel) == 0:
        svc_log_err(f"not is user {[user_name]}")
        return jsonify({"code": Http_status.http_status_server_err, "msg": "用户或密码错误"})
    if not p.decrypt(rel[0][1], password):
        svc_log_err("user input password error")
        return jsonify({"code": Http_status.http_status_server_err, "msg": "用户或密码错误"})
    svc_log_info("user login success")
    if not mg.insert_login_info(user_name):
        svc_log_err("user login info record fail")
    return jsonify({"code": Http_status.http_status_ok, "role": rel[0][2], "username": rel[0][0],
                    "token": create_token(rel[0][0]), })


@user_manage.route("/user/create", methods=['POST'])
@jwt_required()
@check_token
def create_user():
    data = request.get_json()
    username = data.get('user')
    role = data.get('role')
    passwd = data.get('password')
    passwd1 = data.get('password1')
    phone = data.get('phone')
    mailbox = data.get('mailbox')
    if passwd != passwd1:
        return jsonify({'code': Http_status.http_status_server_err, 'msg': '密码输入不一致'})
    try:
        hash_pwd = p.encryption(passwd1)
        cursor.execute("INSERT INTO users (username, role, password, phone, mailbox) VALUES (?, ?, ?, ?, ?)",
                       (username, role, hash_pwd, phone, mailbox))
        svc_log_info(f"create user [{username}] ok")
        return jsonify({'code': Http_status.http_status_ok, "msg": "用户创建成功"})
    except:
        print(traceback.format_exc())
        svc_log_err(f"create user [{username}] fail")
        return jsonify({'code': Http_status.http_status_server_err, "msg": "用户创建失败"})


@user_manage.route("/user/get")
@jwt_required()
@check_token
def get_user():
    rel = s.show_select_rel("SELECT username,role,phone,mailbox  FROM users")
    user_list = data_init(rel)
    # query = request.args.get('query', '')
    pagesize = int(request.args.get('pagesize', 5))
    pagenum = int(request.args.get('pagenum', 1))
    start_index = (pagenum - 1) * pagesize
    end_index = start_index + pagesize
    paginated_users = user_list[start_index:end_index]

    response = {
        'userlist': paginated_users,
        'total': len(user_list)
    }

    return jsonify(response)


@user_manage.route("/user/update", methods=['POST'])
@jwt_required()
@check_token
def update_user():
    data = request.get_json()
    username = data.get('user')
    role = data.get('role')
    phone = data.get('phone')
    try:
        cursor.execute("UPDATE users SET role=? WHERE username=? AND phone=? ", (role, username, phone))
        svc_log_info(f"update user role to [{role}] ok")
        return jsonify({"code": Http_status.http_status_ok, "msg": "修改成功"})
    except:
        print(traceback.format_exc())
        svc_log_err(f"update user role to [{role}] fail")
        return jsonify({"code": Http_status.http_status_server_err, "msg": "修改失败"})


@user_manage.route("/user/delete", methods=['DELETE'])
@jwt_required()
@check_token
def delete_user():
    data = request.get_json()
    username = data.get('user')
    if username == "root":
        return jsonify({"code": Http_status.http_status_server_err, "msg": "不允许删除root"})
    try:
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        svc_log_info(f"delete user ->[{username} ok]")
        if mg.delete_login_info(username):
            svc_log_info(f"delete user [{username}] login info ok")
        else:
            svc_log_err(f"delete user [{username}] login info fail")
        return jsonify({"code": Http_status.http_status_ok, "msg": "删除成功"})
    except:
        print(traceback.format_exc())
        return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败"})


@user_manage.route("/user/search")
@jwt_required()
@check_token
def search_user():
    username = request.args.get('user')
    cursor.execute("SELECT username,role,phone,mailbox  FROM users WHERE username LIKE ?", ('%' + username + '%',))
    rel = cursor.fetchall()
    user_obj = data_init(rel)
    return jsonify({"user_list": user_obj, "total": len(user_obj)})


@user_manage.route("/user/update/passwd", methods=['POST'])
@jwt_required()
@check_token
def update_user_pwd():
    data = request.get_json()
    user_name = data.get('user')
    pwd = data.get('passwd')
    pwd1 = data.get('passwd1')
    if pwd != pwd1:
        return jsonify({'code': Http_status.http_status_server_err, 'msg': '密码输入不一致'})
    try:
        hash_pwd = p.encryption(pwd1)
        cursor.execute("UPDATE users SET password=? WHERE username=?", (hash_pwd, user_name,))
        svc_log_info(f"[{user_name}] update password ok")
        return jsonify({"code": Http_status.http_status_ok, "msg": "修改成功"})
    except:
        print(traceback.format_exc())
        svc_log_err(f"[{user_name}] update password fail")
        return jsonify({"code": Http_status.http_status_server_err, "msg": "修改失败"})


@user_manage.route("/user/center")
@jwt_required()
@check_token
def user_center():
    pass
