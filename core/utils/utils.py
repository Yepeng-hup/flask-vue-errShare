import socket
import requests
from functools import wraps
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
import psutil

from core.svclog import svc_log_err


# 传入列表套元组，转换为列表套字典
def data_init(data) -> list:
    user_list = []
    for i in data:
        u = {
            "user": i[0],
            "role": i[1],
            "phone": i[2],
            "mailbox": i[3]
        }
        user_list.append(u)
    return user_list


# 检测端口是否在线
def check_network_status(host, port) -> bool:
    try:
        # 设置连接超时时间s
        socket.setdefaulttimeout(3)
        socket.create_connection((host, port))
        return True
    except OSError:
        pass
    return False


# 检测服务器localhost存储
def check_server_status() -> list:
    disk_status_list = list()
    disk_partitions = psutil.disk_partitions(all=True)
    for partition in disk_partitions:
        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk_status_obj = {
            "DiskName": partition.device,
            "Total": str(round(disk_usage.total / 1024 / 1024 / 1024))+'G',
            "Used": str(round(disk_usage.used / 1024 / 1024 / 1024))+'G',
            "Free": str(round(disk_usage.free / 1024 / 1024 / 1024))+'G',
            "UsageRate": str(disk_usage.percent)+'%',
        }
        disk_status_list.append(disk_status_obj)
    return disk_status_list


# 检测index
def check_localhost_site(url) -> bool:
    try:
        response = requests.get(url, timeout=3)
        if 200 <= response.status_code < 400:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        svc_log_err(f"errShare site [{url}] fail, {e}")
        return False


# 获取所有路由
def get_all_route() -> list:
    pass


# 生成token
def create_token(user_name) -> str:
    access_token = create_access_token(identity=user_name)
    return access_token




# ######################## 装饰器 #########################


def check_token(func):
    @wraps(func)
    def c(*args, **kwargs):
        user_name = get_jwt_identity()
        if not user_name:
            return jsonify({"auto_status": 0, })
        return func(*args, **kwargs)
    return c
