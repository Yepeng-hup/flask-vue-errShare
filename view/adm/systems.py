import platform
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
import psutil
import os
import datetime
import traceback

from core.utils.utils import check_token, calculate_time
from core.httpStatus import Http_status
from model.secure.search import Search_secure
from core.const import net_status, wink, linux_ps


systems = Blueprint("systems", __name__)
s = Search_secure()


def show_network() -> list:
    netstats = psutil.net_connections()
    network_list = []
    for netstat in netstats:
        try:
            if (netstat.pid == 0) or not netstat.pid:
                continue
            tmp_dict = {}
            tmp_name = psutil.Process(netstat.pid).name()
            # if win or linux
            if platform.system().upper() == 'WINDOWS':
                if tmp_name.upper().replace(' ', '') in wink:
                    continue
            else:
                if tmp_name.upper() in linux_ps:
                    continue
            tmp_dict['process'] = tmp_name
            tmp_dict['pid'] = netstat.pid
            tmp_dict['type'] = ('tcp' if netstat.type == 1 else 'udp')
            tmp_dict['laddr'] = netstat.laddr
            tmp_dict['raddr'] = netstat.raddr or 'None'
            tmp_dict['status'] = net_status.get(netstat.status, netstat.status)
            network_list.append(tmp_dict)
            del (tmp_dict)
        except:
            continue
    return network_list


def show_process() -> list:
    Pids = psutil.pids()
    processList = []
    for pid in Pids:
        try:
            tmp_dict = {}
            tmp_dict['name'] = psutil.Process(pid).name()
            if platform.system().upper() == 'WINDOWS':
                if tmp_dict['name'].upper().replace(' ', '') in wink:
                    continue
            else:
                if tmp_dict['name'].upper() in linux_ps:
                    continue
            tmp_dict['pid'] = pid
            tmp_dict['user'] = os.path.split(psutil.Process(pid).username())[1]
            tmp_dict['memory_percent'] = str(round(psutil.Process(pid).memory_percent(), 2)) + '%'
            processList.append(tmp_dict)
            del (tmp_dict)
        except:
            continue
    process_list = sorted(processList, key=lambda x: x['memory_percent'], reverse=True)
    return process_list


@systems.route("/sys/status/process")
@calculate_time
@jwt_required()
@check_token
def sys_process_status():
    try:
        proc_rel = show_process()
        response_obj = {
            "code": Http_status.http_status_ok,
            "process_list": proc_rel,
        }
        return jsonify(response_obj)
    except:
        print(traceback.format_exc())
        return jsonify({"code": Http_status.http_status_server_err, "msg": "获取资源发生了错误"})


@systems.route("/sys/status/network")
@calculate_time
@jwt_required()
@check_token
def sys_network_status():
    try:
        net_rel = show_network()
        response_obj = {
            "code": Http_status.http_status_ok,
            "network_list": net_rel,
        }
        return jsonify(response_obj)
    except:
        print(traceback.format_exc())
        return jsonify({"code": Http_status.http_status_server_err, "msg": "获取资源发生了错误"})


@systems.route('/sys/status/process/kill', methods=['POST'])
@jwt_required()
@check_token
def kill_process():
    try:
        data = request.get_json()
        pid = data.get('pid')
        p = psutil.Process(int(pid))
        p.kill()
    except Exception as e:
        return jsonify({'code': Http_status.http_status_server_err, 'msg': str(e)})
    else:
        return jsonify({'code': Http_status.http_status_ok, 'msg': 'kill 成功'})


@systems.route('/sys/status/process/info', methods=['POST'])
@jwt_required()
@check_token
def cat_process_info():
    try:
        data = request.get_json()
        pid = data.get('pid')
        p = psutil.Process(int(pid))
        try:
            n = p.exe()
        except:
            n = 'None'
        proIO = p.io_counters()
        process_info = [{
            'ProcessName': p.name(),
            'ProcessPath': n,
            'ProcessStatus': p.status(),
            'ProcessStartTime': datetime.datetime.fromtimestamp(p.create_time()).strftime("%Y-%m-%d %H:%M"),
            'ProcessThreads': p.num_threads(),
            'ProcessCPU': str(p.cpu_percent(0.2)) + '%',
            'ProcessReadCount': proIO.read_count,
            'ProcessWriteCount': proIO.write_count,
            'ProcessReadBytes': proIO.read_bytes,
            'ProcessWriteBytes': proIO.write_bytes
        }]
    except Exception as e:
        return jsonify({'code': Http_status.http_status_server_err, 'mag': str(e)})
    else:
        return jsonify({'code': Http_status.http_status_ok, 'process_info': process_info})


@systems.route("/sys/data")
@jwt_required()
@check_token
def system_data():
    pass
