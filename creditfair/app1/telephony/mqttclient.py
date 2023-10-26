import random
import paho.mqtt.client as mqttclient

broker_address = "10.128.11.3"
port = 1883
user=""
password = ""
token="zjku2Eie3Hv"

def on_connect(client,usedata,flags,rc):
    if rc == 0:
        print("connected Successfully")
        global connected
        connected = True
    else:
        print("connection failed")

client_id = f"mqtt{random.randint(0,999999)}"

client = mqttclient.Client(client_id)
client.username_pw_set(user,password)
client.on_connect = on_connect
client.connect(host=broker_address,port=port)
client.loop_start()

# client = "asdas"