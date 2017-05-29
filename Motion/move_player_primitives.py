import time
import pypot.robot
import pypot.primitive
import numpy
import csv
import random
from kombu import Connection, Exchange, Queue


media_exchange = Exchange('media', 'direct', durable=True)
eye_control_queue = Queue('eye_control', exchange=media_exchange, routing_key='eye_control')

class CustomPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, file="wake_s01"):
        self.robot = robot
        self.file = file
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):

        file = self.file
        print("Playing " + file)

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish(file,
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)
        with open('move/' + file + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':int(float(y)*2), 'm2':int(float(x)*2)}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)


class SleepPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        amp = self.amp
        print("Playing sleep_s01 at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('sleep',
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)
        sleep_pose = {'m1':0, 'm2':50, 'm3':0}
        self.robot.goto_position(sleep_pose,duration=amp, wait=False)
        
class CenterPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        amp = self.amp
        
        center_pose = {'m1':0, 'm2':0, 'm3':0}
        self.robot.goto_position(center_pose,duration=amp, wait=True)