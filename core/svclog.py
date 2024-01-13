from flask import request
from datetime import datetime

current_time = datetime.now()


def svc_log_info(log_str):
    log = "errShare *** [INFO] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    print(log)
    return


def svc_log_err(log_str):
    log = "errShare *** [ERROR] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    print(log)
    return


def svc_log_warn(log_str):
    log = "errShare *** [WARN] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    print(log)
    return
