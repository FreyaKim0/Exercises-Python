# Subscriber

import json
import time
from datetime import datetime
import re
import threading
import paho.mqtt.client as mqtt
from tkinter import *


# print message when received
def on_message(client, userdata, message):
    string_message: str = message.payload.decode("utf-8")   # decode message
    message = json.loads(string_message)                    # convert back to dict
    print_data(message)


def print_data(datadict):
    try:
        # update the figure
        gui.update_figure(datadict)

        # range validation
        if 15 <= datadict['num_students'] <= 40:
            print("Number of students: ", datadict['num_students'])

        # date validation
        month, day, year = datadict['date'].split('/')
        is_date_valid = True
        try:
            datetime(int(year), int(month), int(day))
        except ValueError:
            is_date_valid = False
        if is_date_valid:   # if valid, print date
            print("Class Date: ", datadict['date'])

        # time validation
        is_date_valid = True
        try:
            # regex to validate datetime
            re.match('\d{2}:\d{2}:\d{2}', datadict['time_created'])
        except ValueError:
            is_date_valid = False
        if is_date_valid:   # if valid, print date
            print("Timestamp: ", datadict['time_created'])

        # location validation
        if type(datadict["location"]) == str:
            print("Location: ", datadict['location'])

        print('\n')
    except Exception:       # handle the exception - print Invalid Entry
        print("Data Corrupted - Invalid Entry" + "\n")


class Students(Tk):
    def __init__(self, min_student=15, max_student=40, values=None):
        Tk.__init__(self)
        if values is None:
            values = []
        self.min_student = min_student
        self.max_student = max_student
        self.values = values
        self.lines = []         # lines on the chart
        self.labels = []        # labels that display values
        self.c_width = 500      # canvas width
        self.c_height = 290     # canvas height
        self.c = Canvas(self, width=self.c_width, height=self.c_height, bg='white')  # create canvas
        self.title('Number of students in the class')  # title of the gui
        self.initUI()           # build the gui

    def initUI(self):
        # title of the figure
        self.c.create_text(25, 20, font=("Purisa", 13), anchor=NW, text='Class attendance')
        # figure container
        self.c.create_rectangle(20, self.c_height - 20, 320, 50, fill="#ebebeb", width=0)
        # timestamp text
        self.c.create_text(335, self.c_height - 35, font=("Purisa", 9), anchor=SW, fill='gray', text=f'TimeStamp:')
        self.c.pack(fill=BOTH, expand=1)

    # update the figure using the new value
    def update_figure(self, new_value):
        if len(self.values) >= 20:  # if values array has more than 20 elements
            self.values.pop(0)      # remove the first value

        # add a new key value set(data validation result) to the new_value
        new_value['data_valid'] = True
        # get previous value if self.values's length > 0
        prev_value = self.values[len(self.values) - 1] if len(self.values) > 0 else None

        # range validation (between 15 and 40)
        num_students_valid = True if 15 <= new_value['num_students'] <= 40 else False
        if not num_students_valid:              # if invalid
            new_value['data_valid'] = False     # set data_valid to False
            if prev_value:                      # if previous value is not None, set num_students to previous one
                new_value['num_students'] = prev_value['num_students']
            else:                               # if None, set num_students to 15
                new_value['num_students'] = 15

        # date validation - if float, set date to Invalid date and data_valid to False
        if type(new_value["date"]) == float:
            new_value['date'] = 'Invalid date'
            new_value['data_valid'] = False

        # time validation - if float, set time_created to Invalid timestamp and data_valid to False
        if type(new_value["time_created"]) == float:
            new_value['time_created'] = 'Invalid timestamp'
            new_value['data_valid'] = False

        # time validation - if not string, set location to Invalid location and data_valid to False
        if type(new_value["location"]) != str:
            new_value["location"] = 'Invalid location'
            new_value['data_valid'] = False

        self.values.append(new_value)   # after validation, add the value to the array
        for line in self.lines:         # remove the lines
            self.c.delete(line)
        for label in self.labels:       # remove the labels
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

        y_gap = 20          # the gap between lower canvas edge and x axis
        x0 = 20             # first x coordinate
        x_coordinates = []  # array that stores x coordinate values
        y_coordinates = []  # array that stores y coordinate values

        # add x and y coordinate values to the array
        for i in range(len(self.values)):
            x_coordinates.append(x0)        # add x coordinate value to the array
            y_coordinates.append(           # add y coordinate value to the array
                self.c_height - (self.values[i]['num_students'] / self.max_student * (self.c_height - 120)) - y_gap)
            x0 += 15

        # draw the lines and texts
        for i in range(len(self.values) - 1):
            if self.values[i + 1]['data_valid']:    # Draw a solid line when data is valid
                self.lines.append(
                    self.c.create_line(x_coordinates[i], y_coordinates[i], x_coordinates[i + 1],
                                       y_coordinates[i + 1], fill="#3d6570", width=3))
            else:                                   # Draw a dashed line when data is invalid
                self.lines.append(
                    self.c.create_line(x_coordinates[i], y_coordinates[i], x_coordinates[i + 1],
                                       y_coordinates[i + 1], fill="#3d6570", width=3, dash=(1, 1)))
        self.c.update()  # Update the canvas


# some client name
client_name = "client-sub"
# using local mqtt server as broker
# broker = "127.0.0.1"
# if no local broker available, use open source broker
broker = "mqtt.eclipseprojects.io"

# listening port
port = 1883

# create client
client = mqtt.Client(client_name)
# connect to broker
client.connect(broker, port)

print("Subscribing")
client.subscribe("studentData")  # subscribe to studentData

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