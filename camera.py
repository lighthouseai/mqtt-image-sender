from paho.mqtt import client as mqtt_client
import random,time,json
import base64

broker = 'broker.hivemq.com'
port = 1883
topic = "python/mqtt"
subtopic = "python/get"
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
    print("inside publish++++++++++++++")
    with open("corpimg.png", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        result = client.publish(topic, my_string)
    '''time.sleep(1)
    msg = f"messages: {msg_count}"
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send+++++++++ `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
    msg_count += 1'''

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received++++++++= `{msg.payload.decode()}")
        if msg.payload.decode() != 'proba':
            decodedMsg = json.loads(msg.payload.decode())
            print(decodedMsg['messages'])

            if decodedMsg['messages'] == 'fetch_frame':
                publish(client)
        #print(json.loads(decodedMsg))
        
        #publish(client)
    client.subscribe(subtopic)
    client.on_message = on_message

    

def run():
    client = connect_mqtt()
    client.loop_start()

    #publish(client)
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()