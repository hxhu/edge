# -*- coding: utf-8 -*-
# 以下代码在2019年2月28日 python3.6环境下运行通过
import paho.mqtt.client as mqtt
import json
import time

HOST = "p8e0buw.mqtt.iot.gz.baidubce.com"
PORT = 1883
client_id = "edgeSender"                       # 没有就不写，此处部分内容用xxx代替原内容，下同


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("data/receive")         # 订阅消息

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


def sender(data):
    param = json.dumps(data)
    client = mqtt.Client(client_id)
    client.username_pw_set("p8e0buw/bupt", "QBeYiSPj7p1ZoPZb")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(HOST, PORT, 60)
    print("发送消息:" + param)
    client.publish("up", payload=param, qos=0)     # 发送消息
    client.disconnect() # 必须要关闭


if __name__ == "__main__":
    data = {
        "deviceId": "1234567890",
        "message": "视频信息简介",
        "data": "N1334901317365141504"
    }
    heartbeat = {
        "deviceId": "1234567890",
        "message": "heartbeat", # type
        "data": "1",             # status
        "timestamp": int(time.time())
    }
    sender(heartbeat)
