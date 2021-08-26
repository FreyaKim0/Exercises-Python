# Publisher

from datetime import datetime, timedelta

import group_5_data_generator as data
import json
import time
import random
import paho.mqtt.client as mqtt

# some client name
client_name = "client-pub"
# using local mqtt server as broker
# broker = "127.0.0.1"
# if no local broker available, use open source broker
broker = "mqtt.eclipseprojects.io"

# listening port
port = 1883

# failure chance - 1 in 100
fail_chance = 0.01

# mutate chance - 0.5%
mutate_chance = 0.005

# create a client
client = mqtt.Client(client_name)
# conncect to the broker
print("connecting to broker ", broker)
client.connect(broker, port)

client.loop_start()
# set start date
date = datetime(2020, 1, 1, 0, 0)

# infinite loop
while True:
    d = date.strftime('%m/%d/%Y')
    mydict = data.create_data(d, "Toronto")
    dict_str = json.dumps(mydict)

    # random fail chance, if fail, don't send data
    if random.random() < fail_chance:
        continue

    # random mutate chance, it sends wild data
    if random.random() < mutate_chance:
        mutateDict = {
            "num_students": random.randint(0, 100),
            "date": random.random(),
            "location": random.random(),
            "time_created": random.random()
        }
        dict_str = json.dumps(mutateDict)
        client.publish("studentData", json.dumps(mutateDict))
        print("Just published " + str(dict_str) + " to topic studentData")
        time.sleep(3)
        continue

    # publish data under topic sampledata
    print("publishing ")
    client.publish("studentData", dict_str)
    print("Just published " + str(dict_str) + " to topic studentData")
    date += timedelta(days=1)
    time.sleep(3)  # sleep for 3 seconds before next call