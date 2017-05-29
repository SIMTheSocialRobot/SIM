import time
import pypot.robot
import pypot.primitive
import numpy
import csv
import random
from kombu import Connection, Exchange, Queue


media_exchange = Exchange('media', 'direct', durable=True)
eye_control_queue = Queue('eye_control', exchange=media_exchange, routing_key='eye_control')


class WakePrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        amp = 1
        ver = 1
        print("Playing wake_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('wake_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)
        with open('move/wake_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
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


class ThinkPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        speed = [1.0, 1.5, 2.0, 2.25]
        amp = speed[2] #speed[random.randint(0,3)]
        ver = random.randint(1,4)
        print("Playing think_s0" + str(ver) + " at amp = " + str(amp))
        
        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('think_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)
        with open('move/think_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class YesPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        speed = [0.9, 1.3, 1.6, 1.8]
        amp = speed[3] #speed[random.randint(0,3)]
        ver = random.randint(1,3)
        print("Playing yes_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('yes_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)   
        with open('move/yes_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

      
class NoPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        speed = [1.0, 1.5, 2.0]
        amp = speed[2] #speed[random.randint(0,2)]
        ver = random.randint(1,3)
        print("Playing no_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('no_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/no_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class ShockedPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        speed = [1.0, 1.5, 2.0]
        amp = speed[2] #speed[random.randint(0,2)]
        ver = random.randint(1,2)
        print("Playing shocked_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('shocked_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)
        with open('move/shocked_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class HappyPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, little=False):
        self.robot = robot
        self.little = little
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        little = self.little
        if little is True:
            amp = 0.7
        else:
            speed = [1.0, 1.5, 2.0, 2.3]
            amp = speed[2] #speed[random.randint(0,3)]
        ver = random.randint(1,2)
        print("Playing happy_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('happy_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/happy_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class SadPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, little=False):
        self.robot = robot
        self.little = little
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        little = self.little
        if little is True:
            amp = 0.7
        else:
            speed = [1.0, 1.5, 2.0]
            amp = speed[2] #speed[random.randint(0,2)]
        
        ver = random.randint(1,2)
        print("Playing sad_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('sad_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/sad_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class LittleHappyPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, little=False):
        self.robot = robot
        self.little = little
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        little = self.little
        if little is True:
            amp = 0.7
        else:
            amp = 0.7
        ver = random.randint(1,2)
        print("Playing happy_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('happy_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/happy_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class LittleSadPrimitive(pypot.primitive.Primitive):

    def __init__(self, robot, little=False):
        self.robot = robot
        self.little = little
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        little = self.little
        if little is True:
            amp = 0.7
        else:
            amp = 0.7
        
        ver = random.randint(1,2)
        print("Playing sad_s0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('sad_s0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/sad_s0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class YesPrimitive_D(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        
        amp = 1
        ver = 1
        print("Playing yes_d0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('yes_d0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/yes_d0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

      
class NoPrimitive_D(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        
        amp = 1
        ver = 1
        print("Playing no_d0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('no_d0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/no_d0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)
            
class ThinkPrimitive_D(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        
        amp = 1
        ver = 1
        print("Playing think_d0" + str(ver) + " at amp = " + str(amp))
        
        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('think_d0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/think_d0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class WakePrimitive_D(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        amp = 1
        ver = 1
        print("Playing wake_d0" + str(ver) + " at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('wake_d0' + str(ver),
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        with open('move/wake_d0' + str(ver) + '.move','rb') as csvfile:
            reader = csv.reader(csvfile)
            # next(reader, None)  # skip the headers
            for row in reader:
                x, y = row[0].split()
                next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
                self.robot.goto_position(next_pose,duration=0.09, wait=False)

                time.sleep(0.04)

class SleepPrimitive_D(pypot.primitive.Primitive):

    def __init__(self, robot, amp=1):
        self.robot = robot
        self.amp = amp
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        amp = self.amp
        print("Playing sleep_d01 at amp = " + str(amp))

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('sleep',
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)
        sleep_pose = {'m1':0, 'm2':50, 'm3':0}
        self.robot.goto_position(sleep_pose,duration=amp, wait=False)

class IdlePrimitive(pypot.primitive.Primitive):

    def __init__(self, robot):
        self.robot = robot
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        
            
        print("Playing idle")

        # with Connection('amqp://guest:guest@localhost:5672//') as conn:
        #     producer = conn.Producer(serializer=None)
        #     producer.publish('idle' + str(ver),
        #         exchange=media_exchange, routing_key='eye_control',
        #         declare=[eye_control_queue], durable=True)

        time.sleep(random.randint(0,2))    
        
        sleep_pose = {'m1':random.randint(-10,10), 'm2':random.randint(-10,10), 'm3':random.randint(-8,8)}
        self.robot.goto_position(sleep_pose,duration=0.3, wait=False)

class SwitchStatePrimitive(pypot.primitive.Primitive):

    def __init__(self, robot):
        self.robot = robot
        pypot.primitive.Primitive.__init__(self, robot)
        print('Primitive Initialized')

    def run(self):
        print("Playing switch_state")

        with Connection('amqp://guest:guest@localhost:5672//') as conn:
            producer = conn.Producer(serializer=None)
            producer.publish('switch_state',
                exchange=media_exchange, routing_key='eye_control',
                declare=[eye_control_queue], durable=True)
        time.sleep(1)    
        # with open('move/wake_d0' + str(ver) + '.move','rb') as csvfile:
        #     reader = csv.reader(csvfile)
        #     # next(reader, None)  # skip the headers
        #     for row in reader:
        #         x, y = row[0].split()
        #         next_pose = {'m3':amp*int(float(y)), 'm2':amp*int(float(x))}
        #         self.robot.goto_position(next_pose,duration=0.09, wait=False)