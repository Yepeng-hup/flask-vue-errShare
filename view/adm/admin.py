from flask import Blueprint, jsonify, render_template, request
import re
import os

from model.secure.pwd import Pwd_encryption_decrypt
from core.svclog import svc_log_info
from model.mongo.mgMode import Mg_mode
from core.utils.utils import access_limit
from core.conf import fk_limit_second, fk_limit_number, fk_search_not_str
from model.secure.search import Search_secure


admin = Blueprint("admin", __name__)
p = Pwd_encryption_decrypt()
mg = Mg_mode()
s = Search_secure()


@admin.route("/test", endpoint="test")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="read_send_content")
def tests():
    return jsonify({"code": 200, "msg": "run ok."})


@admin.route("/documents/select/<file_name>", endpoint="read_send_content")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="read_send_content")
def read_send_content(file_name):
    svc_log_info(f"cat file title [{file_name}]")
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    content = mg.select_text({"titel": file_name}, {'text': 1, '_id': 0, 'titel': 1})
    return render_template("front/content.html", content_list=content, all_class_list=all_class)


@admin.route("/search", methods=['POST'], endpoint="admin_search")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="admin_search")
def admin_search():
    search_text = request.form['searchText']
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    if not s.check_search_text(fk_search_not_str, search_text):
        text_list = mg.select_text({'titel': {"$regex": re.compile(search_text)}}, {'text': 0, '_id': 0})
        text_list.reverse()
        return render_template("front/index.html", text_list=text_list, all_class_list=all_class)
    return render_template("front/index.html", text_list=[], all_class_list=all_class)


@admin.route("/choose/<classs>", endpoint="admin_choose")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="admin_choose")
def admin_choose(classs):
    text_list = mg.select_text({'class': classs}, {'text': 0, '_id': 0})
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    text_list.reverse()
    return render_template("front/index.html", text_list=text_list, all_class_list=all_class)


@admin.route("/index", endpoint="admin_index")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="admin_index")   # 限制10秒内最多只能调用4次
def admin_index():
    text_list = mg.select_text({}, {'text': 0, '_id': 0})
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    text_list.reverse()
    return render_template("front/index.html", text_list=text_list, all_class_list=all_class)



