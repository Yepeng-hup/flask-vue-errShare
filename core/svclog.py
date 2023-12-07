from flask import request


def svc_log_info(log_str):
    log = request.remote_addr+" [INFO] "+"---> "+log_str
    print(log)
    return


def svc_log_err(log_str):
    log = request.remote_addr+" [ERROR] "+"---> "+log_str
    print(log)
    return


def svc_log_warn(log_str):
    log = request.remote_addr+" [WARN] "+"---> "+log_str
    print(log)
    return
