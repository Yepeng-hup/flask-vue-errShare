from flask import Blueprint, jsonify, render_template, request
from model.secure.pwd import Pwd_encryption_decrypt
from model.mongo.mgMode import Mg_mode
from core.utils.utils import check_server_status, check_localhost_site


test = Blueprint("test", __name__)

p = Pwd_encryption_decrypt()
mg = Mg_mode()


@test.route("/test")
def test_check():
    if check_localhost_site("http://192.168.1.119:8088/index"):
        print("ok")
    return jsonify({"code": 200})


# @test.route("/tests", methods=['GET', 'POST'])
# def tests_check():
#     user_list = [
#         {"user": "tom", "age": 18, "phone": "15888590777", "mailbox": "15888590777@163.com", "homeAddr": "艾欧尼亚无极村0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"},
#         {"user": "alix", "age": 29, "phone": "15888590766", "mailbox": "15888590766@163.com", "homeAddr": "德玛西亚0号"}]
#     if request.method == "POST":
#         data = request.get_json()
#         username = data.get('user')
#         print("----> ", username, "   all-----> ", data)
#         return jsonify({"post": 200})
#
#     # get分页返回
#     query = request.args.get('query', '')
#     pagesize = int(request.args.get('pagesize', 5))
#     pagenum = int(request.args.get('pagenum', 1))
#     start_index = (pagenum - 1) * pagesize
#     end_index = start_index + pagesize
#     paginated_users = user_list[start_index:end_index]
#
#     response = {
#         'userlist': paginated_users,
#         'total': len(user_list)
#     }
#
#     return jsonify(response)
    # return jsonify({"get": 200, "userlist": user_list, "total": 11})


@test.route("/test/art", methods=['GET', 'POST'])
def show_art():
    # v = check_network_status(mg_host, mg_port)
    # if v:
        vm_db = [
            {"title": "如何部署一套nginx集群", "user": "小明", "classs": "nginx", "label": "nginx,linux", "datetime": "2023-12-22 14:03"},
            {"title": "如何部署一套redis集群", "user": "tom", "classs": "redis", "label": "redis,linux","datetime": "2023-12-12 14:03"},
            {"title": "如何部署一套nginx集群", "user": "小红", "classs": "nginx", "label": "nginx,linux","datetime": "2023-12-22 14:03"},
            {"title": "如何部署一套mysql集群", "user": "小明", "classs": "mysql", "label": "mysql,linux","datetime": "2023-12-10 14:03"},
        ]
        # svc_log_info("network conn check ok.")
        # class_list = ["mongo"]
        # label_list = ["linux", "db"]
        # texts = "我闻琵琶已叹息，又闻此语重唧唧。同是天涯沦落人，相逢何必曾相识！"
        # mg.insert_text("test", "tom", class_list, label_list, texts)
        return jsonify({"code": 200, "wzList": vm_db})
    # else:
    #     return jsonify({"msg": "mongo conn fail"})



# @test.route("/test/class", methods=['GET', 'POST'])
# def show_label():
#     vm_db = [
#         {"className": "nginx", "createDate": "2020-10-11 10:21", "wzMaxNum": "20"},
#         {"className": "golang", "createDate": "2020-10-14 10:21", "wzMaxNum": "2"},
#         {"className": "python", "createDate": "2020-12-11 10:21", "wzMaxNum": "10"},
#     ]
#
#     return jsonify({"code": 200, "classList": vm_db})