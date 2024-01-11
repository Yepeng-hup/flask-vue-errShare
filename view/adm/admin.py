from flask import Blueprint, jsonify, render_template, request
import re


from model.secure.pwd import Pwd_encryption_decrypt
from core.svclog import svc_log_info, svc_log_err
from model.mongo.mgMode import Mg_mode


admin = Blueprint("admin", __name__)
p = Pwd_encryption_decrypt()
mg = Mg_mode()


@admin.route("/test")
def tests():
    return jsonify({"code": 200})


@admin.route("/documents/select/<file_name>")
def read_send_content(file_name):
    svc_log_info(f"cat file title [{file_name}]")
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    content = mg.select_text({"titel": file_name}, {'text': 1, '_id': 0, 'titel': 1})
    return render_template("front/content.html", content_list=content, all_class_list=all_class)


@admin.route("/search", methods=['POST'])
def admin_search():
    search_text = request.form['searchText']
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    text_list = mg.select_text({'titel': {"$regex": re.compile(search_text)}}, {'text': 0, '_id': 0})
    text_list.reverse()
    return render_template("front/index.html", text_list=text_list, all_class_list=all_class)


@admin.route("/choose/<classs>")
def admin_choose(classs):
    text_list = mg.select_text({'class': classs}, {'text': 0, '_id': 0})
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    text_list.reverse()
    return render_template("front/index.html", text_list=text_list, all_class_list=all_class)


@admin.route("/index")
def admin_index():
    text_list = mg.select_text({}, {'text': 0, '_id': 0})
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    text_list.reverse()
    return render_template("front/index.html", text_list=text_list, all_class_list=all_class)



