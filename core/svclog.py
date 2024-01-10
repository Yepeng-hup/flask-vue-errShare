from flask import request
from datetime import datetime

current_time = datetime.now()


def svc_log_info(log_str):
    log = request.remote_addr+" [INFO] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    print(log)
    return


def svc_log_err(log_str):
    log = request.remote_addr+" [ERROR] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    print(log)
    return


def svc_log_warn(log_str):
    log = request.remote_addr+" [WARN] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    print(log)
    return
