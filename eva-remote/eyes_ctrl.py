# python3.6

import random
import socket
import time
import json

from paho.mqtt import client as mqtt_client

HOST = "192.168.1.100"  # IP da XIAMI
PORT = 80  # The port used by the server

topic = "eva/light/+"
broker = '127.0.0.1' #broker.emqx.io'
port = 1883
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


""" def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client): # light state
    print("subscribing")
    def on_message(client, userdata, msg):
        if msg.topic == "eva/light/state":
            if msg.payload.decode() == "on":
                print("msg topic:", msg.topic)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(b'{"id":1, "method":"set_power","params":["on", "smooth", 1000]}\r\n')
                    data = s.recv(1024)
                print(f"Received {data!r}")

            elif msg.payload.decode() == "off":
                print("msg topic:", msg.topic)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(b'{"id":1, "method":"set_power","params":["off", "smooth", 1000]}\r\n')
                    data = s.recv(1024)
                print(f"Received {data!r}")
        

        if msg.topic == "eva/light/color_name":
            color_dec = None
            color_upper = msg.payload.decode().upper() # uppercase é o padrão de constante em XML
            if color_upper == "red".upper(): # uppercase é o padrão de constante em XML
                color_dec = "16711680"
            elif color_upper == "orange".upper():
                color_dec = "16751360"
            elif color_upper == "green".upper():
                color_dec = "65280"
            elif color_upper == "blue".upper():
                color_dec = "255"
            elif color_upper == "yellow".upper():
                color_dec = "16776960"
            elif color_upper == "pink".upper():
                color_dec = "16711935"
            elif color_upper == "white".upper():
                color_dec = "16777215"

            if color_dec != None:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    st = '{"id":1,"method":"set_rgb","params":[' + color_dec + ', "smooth", 1000]}\r\n'
                    s.sendall(bytes(st, 'utf-8'))
                    data = s.recv(1024)
                print(f"Received {data!r}")

            else:
                print("There is something wrong... Please, check the color name!")
        
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run() """

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    time.sleep(10)
    s.connect((HOST, PORT))
    #st = '{"id":1,"method":"set_rgb","params":[' + color_dec + ', "smooth", 1000]}\r\n'
    st = "{ anim: 'anger', bcolor: '', speed: 2 }"
    print(st)

    s.sendall(bytes(st, "utf-8"))
    
#    data = s.recv(1024)
#print(f"Received {data!r}")
print("Conectado")