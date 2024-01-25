import socket
import requests
from functools import wraps
from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
import psutil
import time
import re
import os
import traceback
from bs4 import BeautifulSoup

from core.svclog import svc_log_err, svc_log_info
from core.httpStatus import Http_status
from core.conf import fk_limit_start
from model.sqlite.select import Select_tables

s = Select_tables()


################################ 工具函数 #########################################################

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


def data_init_rel(data, dict_) -> list:
    l = []
    for i in data:
        u = dict_
        l.append(u)
    return l


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
            "Total": str(round(disk_usage.total / 1024 / 1024 / 1024)) + 'G',
            "Used": str(round(disk_usage.used / 1024 / 1024 / 1024)) + 'G',
            "Free": str(round(disk_usage.free / 1024 / 1024 / 1024)) + 'G',
            "UsageRate": str(disk_usage.percent) + '%',
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


# delete img
def delete_not_text_img(html_content):
    img_del_src_list = []
    img_del_name_lsit = []
    soup = BeautifulSoup(html_content, 'html.parser')
    # 获取img标签中的src元素值
    images = soup.find_all('img')
    for img in images:
        src = img['src']
        img_del_src_list.append(src)

    for i in img_del_src_list:
        result = re.search(r'/([^/]+)$', i)
        if result:
            img_name = result.group(1)
            img_del_name_lsit.append(img_name)
        else:
            pass

    if len(img_del_name_lsit) >= 1:
        for n in img_del_name_lsit:
            try:
                os.remove("./upload/images/" + n)
                svc_log_info(f"delete images ok -> [{n}]")
            except:
                svc_log_err(f"delete images fail -> [{n}]")
                print(traceback.format_exc())
    return


def delete_not_text_video(html_content):
    video_del_src_list = []
    video_del_name_lsit = []
    soup = BeautifulSoup(html_content, 'html.parser')
    videos = soup.find_all('source')
    for video in videos:
        src = video['src']
        video_del_src_list.append(src)

    for i in video_del_src_list:
        result = re.search(r'/([^/]+)$', i)
        if result:
            video_name = result.group(1)
            video_del_name_lsit.append(video_name)
        else:
            pass

    if len(video_del_name_lsit) >= 1:
        for n in video_del_name_lsit:
            try:
                os.remove("./upload/video/" + n)
                svc_log_info(f"delete video ok -> [{n}]")
            except:
                svc_log_err(f"delete video fail -> [{n}]")
                print(traceback.format_exc())
    return


def show_all_user_num() -> int:
    rel = s.show_select_rel("SELECT username FROM users")
    if len(rel) <= 0:
        return 0
    return len(rel)


def run_linux_code(run_code) -> bool:
    x = os.system(run_code)
    if x == 0:
        return True
    return False


def delete_lines(filepath, target) -> bool:
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()

        temp_filename = f"{os.path.splitext(filepath)[0]}_tmp.txt"
        with open(temp_filename, 'w') as temp_file:
            for line in lines:
                if target not in line:
                    temp_file.write(line)

        # 将临时文件重命名为原始文件
        os.remove(filepath)
        os.rename(temp_filename, filepath)
        return True
    except:
        print(traceback.format_exc())
        return False


# ######################## 装饰器 #########################


def check_token(func):
    @wraps(func)
    def c(*args, **kwargs):
        user_name = get_jwt_identity()
        if not user_name:
            return jsonify({"auto_status": 0, })
        return func(*args, **kwargs)

    return c


def access_limit(max_calls, period, api_name=None):
    def decorator(func):
        call_times = []

        def wrapper(*args, **kwargs):
            if fk_limit_start == "YES":
                current_time = time.time()
                call_times.append(current_time)
                # 移除超时窗口的调用时间
                call_times[:] = [t for t in call_times if t > current_time - period]
                if len(call_times) > max_calls:
                    svc_log_err(f"API [{api_name}] calls exceeded limit, please try again later.")
                    return jsonify(
                        {
                            "code": Http_status.http_status_server_err,
                            "status": "error",
                            "msg": "Frequent visits, retry after 3 seconds.",
                        }
                    )
                else:
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def calculate_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        svc_log_info(f"function name: {func.__name__} runtime: {end_time - start_time} s")
        return result

    return wrapper
