# -*- coding: utf-8 -*-
# 接收到的消息分发
import json
import time
import threading
from pydash import get, set_
from ftp_client import pushModel, fileModel
from mqtt_sender import sender
from device_info import total_load

# 消息例子
# {"command":"pushModel;points","data":"/home/ftpdir/models/yolov3.weights;N1334859111304531968","target":["N1334896073990213632","1234567890"],"timestamp":1607944867,"extra":{"pattern":"I"}} //I(立即) F(闲时) S(指定)


def distributor(msg):
    flag = True
    msg_json = json.loads(str(msg.payload.decode('utf-8')))

    # 排除之前的消息
    now_time = int(time.time())
    get_time = (int(get(msg_json, "timestamp", 0)) / 1000) if (int(get(msg_json, "timestamp", 0)) > 1000000000000) else int(get(msg_json, "timestamp", 0))
    if (now_time - get_time) >= 600 or (now_time - get_time) < 0:
        flag = False

    # 确定是自己的消息,编号为1234567890
    device_id = "1234567890"
    if (device_id not in get(msg_json, "target", [])) and (get(msg_json, "target", []) != "null"):
        flag = False

    if flag:
        print("=====消息分发器=====")
        print(msg_json)
         
        # 提取command,data,extra
        command_split = get(msg_json, "command", []).split(";")
        data_split = get(msg_json, "data", []).split(";")
        extra = get(msg_json, "extra", [])

        # 模型推送
        if get(command_split, '0', "") == "pushModel":
            tuple_data = {
                "command_split": command_split, 
                "data_split": data_split, 
                "msg_json": msg_json, 
                "device_id": device_id,
                "extra": extra
            }
            thread = threading.Thread(target = model_push, kwargs = tuple_data)
            thread.start()

        # 文件推送
        if get(command_split, '0', "") == "pushFile":
            tuple_data = {
                "command_split": command_split, 
                "data_split": data_split, 
                "msg_json": msg_json, 
                "device_id": device_id,
                "extra": extra
            }
            thread = threading.Thread(target = file_push, kwargs = tuple_data)
            thread.start()


# 模型推送
def model_push(**kwargs):
    print(kwargs)
    # 数据处理
    command_split = get(kwargs, "command_split")
    data_split = get(kwargs, "data_split")
    msg_json = get(kwargs, "msg_json")
    device_id = get(kwargs, "device_id")
    extra = get(kwargs, "extra")

    # 指定推送
    if command_split[1] == "points":
        if pushModel(get(msg_json, "data", "")):
            send_data = {}

            set_(send_data, "deviceId", device_id)
            set_(send_data, "message", "modelUpdate")  # type 说明是模型更新了
            set_(send_data, "data", get(data_split, "1", ""))  # modelId
            set_(send_data, "timestamp", int(time.time()))

            waiting(extra)

            # {"deviceId": "1234567890", "message": "modelUpdate", "data": "N1334859111304531968", "timestamp": 1607966540}
            sender(send_data)
    # 广播推送
    elif command_split[1] == "all":
        if pushModel(get(msg_json, "data", "")):
            i = 0
    
    print("\n")


# 文件推送
def file_push(**kwargs):
    # 数据处理
    command_split = get(kwargs, "command_split")
    data_split = get(kwargs, "data_split")
    msg_json = get(kwargs, "msg_json")
    device_id = get(kwargs, "device_id")
    extra = get(kwargs, "extra")

    # 指定推送
    if command_split[1] == "points":
        if fileModel(get(msg_json, "data", "")):
            send_data = {}

            set_(send_data, "deviceId", device_id)
            set_(send_data, "message", "fileUpdate")  # type 说明是模型更新了
            set_(send_data, "data", get(data_split, "1", ""))  # fileId
            set_(send_data, "timestamp", int(time.time()))

            waiting(extra)

            # {"deviceId": "1234567890", "message": "modelUpdate", "data": "N1334859111304531968", "timestamp": 1607966540}
            sender(send_data)
    # 广播推送
    elif command_split[1] == "all":
        if pushModel(get(msg_json, "data", "")):
            i = 0
    
    print("\n")


# 下载等待
def waiting(extra):
    print(extra)
    pattern = get(extra, "pattern", "F")
    if pattern == "I":    # 立即更新
        print("立即更新模型")
    elif pattern == "F":  # 闲时更新
        print("等待闲时更新...")
        '''
        <闲时定义> 
            CPU使用率: 0.7
            内存使用率
            负载信息
            当前网速
        '''
        while True:
            if total_load():
                break
    elif pattern == "S":  # 指定时间更新
        print("指定更新时间..." + time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(get(extra, "data", int(time.time())))))
        
        while True:
            if get(extra, "data", int(time.time())) <= int(time.time()):
                print("开始下载...")
                break
        
    