from flask import Blueprint, jsonify, render_template, request
import re

from model.secure.pwd import Pwd_encryption_decrypt
from core.svclog import svc_log_info
from model.mongo.mgMode import Mg_mode
from core.utils.utils import access_limit
from core.conf import fk_limit_second, fk_limit_number, fk_search_not_str
from model.secure.search import Search_secure
from core.httpStatus import Http_status

admin = Blueprint("admin", __name__)
p = Pwd_encryption_decrypt()
mg = Mg_mode()
s = Search_secure()


@admin.route("/health")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="read_send_content")
def tests():
    return jsonify({"code": Http_status.http_status_ok, "msg": "run ok."})


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
    return render_template("front/index.html", text_list=[], all_class_list=all_class,
                           info="error: search content illegality")


@admin.route("/choose/<classs>", endpoint="admin_choose")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="admin_choose")
def admin_choose(classs):
    text_list = mg.select_text({'class': classs}, {'text': 0, '_id': 0})
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    text_list.reverse()
    return render_template("front/index.html", text_list=text_list, all_class_list=all_class)


@admin.route("/index", endpoint="admin_index")
@access_limit(max_calls=fk_limit_number, period=fk_limit_second, api_name="admin_index")
def admin_index():
    text_list = mg.select_text({}, {'text': 0, '_id': 0})
    all_class = mg.select_all_class({'_id': 0, 'date': 0})
    text_list.reverse()
    # pagesize = 10
    # pagenum = int(request.args.get('pagenum', 1))
    # start_index = (pagenum - 1) * pagesize
    # end_index = start_index + pagesize
    # paginated_text = text_list[start_index:end_index]
    # paginated_text.reverse()
    # rel_list = list(str(len(text_list) / 10).split('.'))
    # if int(rel_list[1]) == 0:
    #     return render_template("front/index.html", text_list=paginated_text, all_class_list=all_class,
    #                            page_total=int(rel_list[0]) + 1)
    return render_template("front/index.html", text_list=text_list, all_class_list=all_class)
