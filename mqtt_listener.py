# pip install paho-mqtt
# 百度云服务器 Iot-Hub
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import json
import time

HOST = "p8e0buw.mqtt.iot.gz.baidubce.com"
PORT = 1883
client_id = "edgeListener"                       # 没有就不写，此处部分内容用xxx代替原内容，下同


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("down")         # 订阅消息


def on_message(client, userdata, msg):
    print("topic:" + msg.topic + " message:" + str(msg.payload.decode('utf-8')))


def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


def listener():
    # param = json.dumps(data)
    client = mqtt.Client(client_id)
    client.username_pw_set("p8e0buw/bupt", "QBeYiSPj7p1ZoPZb")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.connect(HOST, PORT, 60)
    client.subscribe("down", 0)
    client.loop_forever()

if __name__ == "__main__":
    listener()