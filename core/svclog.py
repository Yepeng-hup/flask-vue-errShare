from datetime import datetime

current_time = datetime.now()


def log_write_file(log):
    with open('log/errshare.log', 'a') as file:
        file.write(f'{log}\n')
    return


def svc_log_info(log_str):
    log = "errShare *** [INFO] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    log_write_file(log)
    return


def svc_log_err(log_str):
    log = "errShare *** [ERROR] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    log_write_file(log)
    return


def svc_log_warn(log_str):
    log = "errShare *** [WARN] "+"["+current_time.strftime("%Y-%m-%d %H:%M:%S")+"]"+" --> "+log_str
    log_write_file(log)
    return
