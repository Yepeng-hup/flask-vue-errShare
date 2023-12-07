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