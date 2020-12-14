# -*- coding: utf-8 -*-
import time
from pydash import set_
from mqtt_sender import sender

# heartbeat = {
#     "deviceId": "1234567890",
#     "message": "heartbeat",  # type
#     "data": "1",             # status
#     "timestamp": int(time.time())
# }
# 每隔5秒发送一次心跳


def send_heartbeat(interval):
    while(True):
        device_id = "1234567890"
        data_type = "heartbeat"
        status = "1"  # 通过检测获得状态
        timestamp = int(time.time())
        heartbeat = {}

        set_(heartbeat, "deviceId", device_id)
        set_(heartbeat, "message", data_type)
        set_(heartbeat, "data", status)
        set_(heartbeat, "timestamp", timestamp)
        
        sender(heartbeat) # 发送

        time.sleep(interval)  # 休眠interval秒


if __name__ == "__main__":
    send_heartbeat(5)
