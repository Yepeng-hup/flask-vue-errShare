from flask import Blueprint, jsonify, request, send_file
import traceback
from flask_jwt_extended import jwt_required
from datetime import datetime
import os
import copy
import re

from model.mongo.mgMode import Mg_mode
from core.utils.utils import check_token
from core.conf import fk_upload_ip_domain, fk_port
from core.httpStatus import Http_status
from core.svclog import svc_log_info, svc_log_err

article_manage = Blueprint("article_manage", __name__)
mg = Mg_mode()


@article_manage.route("/wz/upload/images", methods=['POST'])
def wz_upload_images():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    save_path = "static/upload/images/"
    images = request.files['file']
    if images:
        save_name = formatted_time + "-" + images.filename
        url = "http://" + fk_upload_ip_domain + ":" + str(fk_port) + "/" + save_path + save_name
        images.save(save_path + save_name)
        return jsonify({
            "errno": 0,
            "data": {
                "url": url,
                "alt": save_name,
            }
        })
    else:
        return jsonify({
            "errno": 1,
            "message": "file and images push fail."
        })


@article_manage.route("/wz/upload/video", methods=['POST'])
def wz_upload_video():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    save_path = "static/upload/video/"
    video = request.files['video']
    if video:
        save_name = formatted_time + "-" + video.filename
        url = "http://" + fk_upload_ip_domain + ":" + str(fk_port) + "/" + save_path + save_name
        video.save(save_path + save_name)
        return jsonify({
            "errno": 0,
            "data": {
                "url": url,
            }
        })
    else:
        return jsonify({
            "errno": 1,
            "message": "video push fail."
        })


@article_manage.route("/wz/w", methods=['POST'])
# @jwt_required()
# @check_token
def wz_set():
    data = request.get_json()
    user = data.get('user')
    title = data.get("title")
    classs = data.get('classs')
    label = data.get('label')
    content = data.get('textHtml')
    if title == '' or classs == '' or content == '':
        return jsonify({"code": Http_status.http_status_server_err})
    b = mg.insert_text(title, user, classs, label, content)
    if not b:
        return jsonify({"code": Http_status.http_status_server_err})
    return jsonify({"code": Http_status.http_status_ok, "msg": "发布成功"})


@article_manage.route("/wz/r")
def wz_read():
    text_list = mg.select_text({}, {'text': 0, '_id': 0})
    return jsonify({"code": Http_status.http_status_ok, "wzList": text_list, 'num': len(text_list)})


@article_manage.route("/wz/d", methods=['DELETE'])
def wz_delete():
    content_list = list()
    data = request.get_json()
    title_name = data.get('titel')
    text_list = mg.select_text({'titel': title_name}, {'_id': 0})
    for k in text_list[0]:
        content_list.append(text_list[0][k])
    # 先写入回收站
    if not mg.insert_recovery(content_list[0], content_list[1], content_list[2], content_list[3], content_list[4],
                              content_list[5]):
        return jsonify({"code": Http_status.http_status_server_err, "msg": "回收失败"})
    # 执行text集合文本删除
    if not mg.delete_text(title_name):
        svc_log_err(f"delete text fail --> [{title_name}]")
        return jsonify({"code": Http_status.http_status_server_err, "msg": "回收失败"})
    return jsonify({"code": Http_status.http_status_ok, "msg": "回收成功"})


@article_manage.route("/wz/edit", methods=['POST'])
def text_edit():
    data = request.get_json()
    pass


@article_manage.route("/wz/s", methods=['POST'])
def text_search():
    data = request.get_json()
    search_name = data.get('searchTxt')
    text_list = mg.select_text({'titel': {"$regex": re.compile(search_name)}}, {'text': 0, '_id': 0})
    return jsonify({"code": Http_status.http_status_ok, "wz_list": text_list, 'num': len(text_list)})


@article_manage.route("/wz/class/w", methods=['POST'])
def class_set():
    data = request.get_json()
    class_name = data.get('class')
    if class_name == '':
        return jsonify({"code": Http_status.http_status_server_err})
    b = mg.insert_class(class_name)
    if not b:
        return jsonify({"code": Http_status.http_status_server_err})
    return jsonify({"code": Http_status.http_status_ok, "msg": "创建成功"})


@article_manage.route("/wz/class/r")
def class_read():
    rel = mg.select_all_class({'_id': 0})
    deep_copy_rel_list = copy.deepcopy(rel)
    for c in rel:
        class_num = mg.select_wz_num({"class": c['class']})
        for d in deep_copy_rel_list:
            if c['class'] == d['class']:
                d.update({'num': class_num})
                break
    return jsonify({"code": Http_status.http_status_ok, "classList": deep_copy_rel_list})


@article_manage.route("/wz/class/show")
def class_show():
    class_list = list()
    rel = mg.select_all_class({'_id': 0, 'date': 0})
    for i in rel:
        d = {"value": i['class'], "label": i['class']}
        class_list.append(d)
    boj_data = {
        "wz_class": class_list
    }
    return jsonify(boj_data)


@article_manage.route("/wz/class/screen", methods=['POST'])
def class_screen():
    data = request.get_json()
    class_name = data.get('class')
    text_list = mg.select_text({'class': class_name}, {'text': 0, '_id': 0})
    return jsonify({"code": Http_status.http_status_ok, "wz_list": text_list, "num": len(text_list)})


@article_manage.route("/wz/class/d", methods=['DELETE'])
def class_delete():
    data = request.get_json()
    class_name = data.get('class')
    text_list = mg.select_text({'class': class_name}, {'text': 0, '_id': 0})
    if len(text_list) > 0:
        return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败,有关联文章"})
    if not mg.delete_class(class_name):
        return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败"})
    return jsonify({"code": Http_status.http_status_ok, "msg": "删除成功"})


@article_manage.route("/wz/label/w", methods=['POST'])
def label_set():
    data = request.get_json()
    label_name = data.get('label')
    if label_name == '':
        return jsonify({"code": Http_status.http_status_server_err})
    b = mg.insert_label(label_name)
    if not b:
        return jsonify({"code": Http_status.http_status_server_err})
    return jsonify({"code": Http_status.http_status_ok, "msg": "创建成功"})


@article_manage.route("/wz/label/r")
def label_read():
    rel = mg.select_all_label({'_id': 0})
    deep_copy_rel_list = copy.deepcopy(rel)
    for c in rel:
        label_num = mg.select_wz_num({"label": c['label']})
        for d in deep_copy_rel_list:
            if c['label'] == d['label']:
                d.update({'num': label_num})
                break
    return jsonify({"code": Http_status.http_status_ok, "labelList": deep_copy_rel_list})


@article_manage.route("/wz/label/show")
def label_show():
    label_list = list()
    rel = mg.select_all_label({'_id': 0, 'date': 0})
    for i in rel:
        d = {"value": i['label'], "label": i['label']}
        label_list.append(d)
    boj_data = {
        "wz_label": label_list
    }
    return jsonify(boj_data)


@article_manage.route("/wz/label/d", methods=['DELETE'])
def label_delete():
    data = request.get_json()
    label_name = data.get('label')
    text_list = mg.select_text({'label': label_name}, {'text': 0, '_id': 0})
    if len(text_list) > 0:
        return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败,有关联文章"})
    if not mg.delete_label(label_name):
        return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败"})
    return jsonify({"code": Http_status.http_status_ok, "msg": "删除成功"})


@article_manage.route("/wz/recovery/r")
def recovery_read():
    rel = mg.select_recovery_text({}, {'text': 0, '_id': 0})
    return jsonify({"code": Http_status.http_status_ok, "recover_list": rel, "num": len(rel)})


@article_manage.route("/wz/recovery/d", methods=['DELETE'])
def recovery_delete():
    data = request.get_json()
    titel_name = data.get('titel')
    if not mg.delete_recovery_text(titel_name):
        return jsonify({"code": Http_status.http_status_server_err, "msg": "删除失败"})
    return jsonify({"code": Http_status.http_status_ok, "msg": "删除成功"})


@article_manage.route("/wz/recovery/c", methods=['POST'])
def recovery_revoke():
    content_list = []
    data = request.get_json()
    title_name = data.get('titel')
    text_list = mg.select_recovery_text({'titel': title_name}, {'_id': 0, 'date': 0, })
    for k in text_list[0]:
        content_list.append(text_list[0][k])
    print(content_list)
    if not mg.insert_text(content_list[0], content_list[1], content_list[2], content_list[3], content_list[4]):
        return jsonify({"code": Http_status.http_status_server_err, "msg": "撤消失败"})
    if not mg.delete_recovery_text(title_name):
        return jsonify({"code": Http_status.http_status_server_err, "msg": "撤消失败"})
    return jsonify({"code": Http_status.http_status_ok, "msg": "撤消成功"})


