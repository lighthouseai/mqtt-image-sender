from paho.mqtt import client as mqtt_client
import random,time,json
import base64


broker = 'broker.hivemq.com'
port = 1883
subtopic = "python/mqtt"
topic = "python/get"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

username = 'broker'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    #msg_count = 0
    msg = {"messages": 'fetch_frame'}
    result = client.publish(topic, json.dumps(msg))
    subscribe(client)
    print(result)
    # result: [0, 1]
    '''status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1'''

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("inside on message")

        if msg.payload.decode() !='proba':
            print(type(msg.payload.decode()))
            with open("newone.png", "wb") as fh:
                fh.write(base64.b64decode(msg.payload.decode()))
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(subtopic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_forever()


if __name__ == '__main__':
    run()