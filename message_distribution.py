 # -*- coding: utf-8 -*-
 # 接收到的消息分发
import json
import time
from pydash import get
from ftp_client import pushModel

# 消息例子
# {"command":"pushModel;points","data":"/home/ftpdir/models/yolov3.weights;N1334859111304531968","target":["N1334896073990213632","1234567890"],"timestamp":1607944867}
def distributor(msg):
    flag = True
    msg_json =  json.loads( str(msg.payload.decode('utf-8')) )
    
    # 排除之前的消息
    now_time = int(time.time())
    get_time = int(get(msg_json, "timestamp", 0) )
    if ( now_time - get_time ) >= 600 or ( now_time - get_time ) < 0:
        flag = False
    
    # 确定是自己的消息,编号为1234567890
    device_id = "1234567890"
    if (device_id not in get(msg_json, "target", [])) and (get(msg_json, "target", []) != "null"):
        flag = False
    
    if flag:
        print("=====消息分发器=====")
        print(msg_json)

        # 提取command
        command_split = get(msg_json, "command", []).split(";")
        # 模型推送
        if get(command_split, '0', "") == "pushModel":
            # 指定推送
            if command_split[1] == "points":
                pushModel(get(msg_json, "data", ""))
            # 广播推送
            elif command_split[1] == "all":
                pushModel(get(msg_json, "data", ""))