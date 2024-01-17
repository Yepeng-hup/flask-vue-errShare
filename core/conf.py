import yaml
import os
import traceback
import config

yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config.check_file())


def read_yaml():
    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except:
        print(traceback.format_exc())


y = read_yaml()
_svc = y.get("errshare")
fk_host = _svc.get("ip")
fk_port = _svc.get("port")
fk_debug = _svc.get("debug")
fk_upload_ip_domain = _svc.get("upload_ip_domain")
fk_ssl_type = _svc.get("ssl_type")
fk_limit_start = _svc.get("limit_start")
fk_limit_number = _svc.get("limit_number")
fk_limit_second = _svc.get("limit_second")
fk_secret_key = _svc.get("secret_key")
fk_jwt_secret_key = _svc.get("jwt_secret_key")
fk_jwt_token_expires_time = _svc.get("jwt_token_expires_time")
fk_timezone = _svc.get("timezone")
fk_search_not_str = _svc.get("search_not_str")

_mongo = y.get("mongodb")
mg_host = _mongo.get("ip")
mg_port = _mongo.get("port")
mg_name = _mongo.get("db_name")
mg_user = _mongo.get("db_user")
mg_password = _mongo.get("db_password")
