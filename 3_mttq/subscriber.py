import json
import time
from datetime import datetime
import re
import threading
import paho.mqtt.client as mqtt
from tkinter import *

# Receive message
def on_message(client, userdata, message):
    string_message: str = message.payload.decode("utf-8") 
    message = json.loads(string_message)                 
    print_data(message)

def print_data(datadict):
    try:
        # update the figure
        gui.update_figure(datadict)
        print('\n')
    except Exception:      
        print("Data Corrupted - Invalid Entry" + "\n")

class Students(Tk):
    def __init__(self, min_student=15, max_student=40, values=None):
        Tk.__init__(self)
        if values is None:
            values = []
        self.min_student = min_student
        self.max_student = max_student
        self.values = values
        self.lines = []         
        self.labels = []       
        self.c_width = 500     
        self.c_height = 290    
        self.c = Canvas(self, width=self.c_width, height=self.c_height, bg='white')  
        self.title('Number of students in the class')  
        self.initUI()       

    def initUI(self):
        self.c.create_text(25, 20, font=("Purisa", 13), anchor=NW, text='Class attendance')
        self.c.create_rectangle(20, self.c_height - 20, 320, 50, fill="#ebebeb", width=0)
        self.c.create_text(335, self.c_height - 35, font=("Purisa", 9), anchor=SW, fill='gray', text=f'TimeStamp:')
        self.c.pack(fill=BOTH, expand=1)

    def update_figure(self, new_value):
        if len(self.values) >= 20:  
            self.values.pop(0)     

        # add a new key value set(data validation result) to the new_value
        new_value['data_valid'] = True
        # get previous value if self.values's length > 0
        prev_value = self.values[len(self.values) - 1] if len(self.values) > 0 else None

        self.values.append(new_value)   
        for line in self.lines:         
            self.c.delete(line)
        for label in self.labels:       
            self.c.delete(label)

        # create the date, location, number of students and timestamp labels
        self.labels.append(
            self.c.create_text(335, 60, font=("Purisa", 9), anchor=NW, text=f'Date: {new_value["date"]}'))
        self.labels.append(
            self.c.create_text(335, 90, font=("Purisa", 9), anchor=NW, text=f'Location: {new_value["location"]}'))
        self.labels.append(self.c.create_text(335, 120, font=("Purisa", 9), anchor=NW,
                                              text=f'Number of students: '
                                                   f'{new_value["num_students"] if num_students_valid else "--"}'))
        self.labels.append(self.c.create_text(335, self.c_height - 20, font=("Purisa", 8), anchor=SW, fill='gray',
                                              text=f'{new_value["time_created"]}'))

        y_gap = 20          
        x0 = 20            
        x_coordinates = []  
        y_coordinates = []  

        for i in range(len(self.values)):
            x_coordinates.append(x0)       
            y_coordinates.append(          
                self.c_height - (self.values[i]['num_students'] / self.max_student * (self.c_height - 120)) - y_gap)
            x0 += 15

        # draw the lines and texts
        for i in range(len(self.values) - 1):
            if self.values[i + 1]['data_valid']:    
                self.lines.append(
                    self.c.create_line(x_coordinates[i], y_coordinates[i], x_coordinates[i + 1],
                                       y_coordinates[i + 1], fill="#3d6570", width=3))
            else:                                  
                self.lines.append(
                    self.c.create_line(x_coordinates[i], y_coordinates[i], x_coordinates[i + 1],
                                       y_coordinates[i + 1], fill="#3d6570", width=3, dash=(1, 1)))
        self.c.update()  

# Connect to open source broker
# -----------------------------
client_name = "client-sub"
broker = "mqtt.eclipseprojects.io"
port = 1883
client = mqtt.Client(client_name)
client.connect(broker, port)
print("Subscribing")
client.subscribe("studentData")  
# -----------------------------

client.on_message = on_message  # attach on message method
gui = Students(15, 40)          # create the app
time.sleep(3)

# create a thread to run the subscriber client
t1 = threading.Thread(target=client.loop_forever(), daemon=True, args=[])
# create a thread to run the tkinter
t2 = threading.Thread(target=gui.mainloop(), daemon=True, args=[])
t1.start()  # start the threads
t2.start()
t1.join()  # join the threads
t2.join()