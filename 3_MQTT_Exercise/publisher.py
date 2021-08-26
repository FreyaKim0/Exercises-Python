from datetime import datetime, timedelta

import data_generator as data
import json
import time
import random
import paho.mqtt.client as mqtt

# Connect to open source broker
# -----------------------------
client_name = "client_name"
broker = "mqtt.eclipseprojects.io"
port = 1883

client = mqtt.Client(client_name)
print("Publisher: Broker connected.", broker)
client.connect(broker, port)
client.loop_start()
# -----------------------------

fail_chance = 0.01
mutate_chance = 0.005
date = datetime(2021, 8, 26, 0, 0)

while True:
    # Generate data
    d = date.strftime('%m/%d/%Y')
    mydict = data.create_data(d, "401 Highway")
    dict_str = json.dumps(mydict)

    # If data fail, don't send data
    if random.random() < fail_chance:
        continue

    # If mutate, sends wild data
    if random.random() < mutate_chance:
        mutateDict = {
            "num_cars": random.randint(0, 100),
            "date": random.random(),
            "location": random.random(),
            "time_created": random.random()
        }
        dict_str = json.dumps(mutateDict)
        client.publish("TrafficData", json.dumps(mutateDict))
        print("Just published " + str(dict_str) + " to trafficData")
        time.sleep(3)
        continue

    # publish data
    print("publishing...")
    client.publish("TrafficData", dict_str)
    print("Data published: " + str(dict_str))
    date += timedelta(days=1)
    time.sleep(3)