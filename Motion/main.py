import pypot.robot
import time
import random
import itertools, numpy
import subprocess
import threading
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
import json

from primitive_library import CenterPrimitive, SleepPrimitive, WakePrimitive, ThinkPrimitive 
from primitive_library import YesPrimitive, NoPrimitive, HappyPrimitive, SadPrimitive, ShockedPrimitive
from primitive_library import YesPrimitive_D, NoPrimitive_D, WakePrimitive_D, ThinkPrimitive_D, SleepPrimitive_D
from primitive_library import LittleHappyPrimitive, LittleSadPrimitive, IdlePrimitive, SwitchStatePrimitive

media_exchange = Exchange('media', 'direct', durable=True)
face_detector_queue = Queue('face_detector', exchange=media_exchange, routing_key='face_detector')
command_queue = Queue('command', exchange=media_exchange, routing_key='command')
eye_control_queue = Queue('eye_control', exchange=media_exchange, routing_key='eye_control')
move_coordinates_queue = Queue('move_coordinates', exchange=media_exchange, routing_key='move_coordinates')

sim = pypot.robot.from_json('sim_config.json')
# Sleep Primitive
sim.attach_primitive(SleepPrimitive(sim,amp=1), 'sleep_s')
sim.attach_primitive(SleepPrimitive_D(sim,amp=1), 'sleep_d')

# Center Primitive
sim.attach_primitive(CenterPrimitive(sim,amp=0.3), 'center')

# Wake Primitive
sim.attach_primitive(WakePrimitive(sim,amp=1), 'wake_s')
sim.attach_primitive(WakePrimitive_D(sim,amp=1), 'wake_d')


# Think Primitives
sim.attach_primitive(ThinkPrimitive(sim,amp=1), 'think_s')
sim.attach_primitive(ThinkPrimitive_D(sim,amp=1), 'think_d')

# Yes Primitives
sim.attach_primitive(YesPrimitive(sim,amp=2), 'yes_s')
sim.attach_primitive(YesPrimitive_D(sim,amp=2,), 'yes_d')

# No Primitives
sim.attach_primitive(NoPrimitive(sim,amp=2), 'no_s')
sim.attach_primitive(NoPrimitive_D(sim,amp=2), 'no_d')

# Shocked Primitives
sim.attach_primitive(ShockedPrimitive(sim,amp=2), 'shocked_s')

# Happy Primitives
sim.attach_primitive(HappyPrimitive(sim), 'happy_s')
sim.attach_primitive(LittleHappyPrimitive(sim,little=True), 'littlehappy_s')


# Sad Primitives
sim.attach_primitive(SadPrimitive(sim), 'sad_s')
sim.attach_primitive(LittleSadPrimitive(sim, little=True), 'littlesad_s')

# Shocked Primitives
sim.attach_primitive(IdlePrimitive(sim), 'idle')

# SwitchState Primitives
sim.attach_primitive(SwitchStatePrimitive(sim), 'switch_state')





sim.center.start()
time.sleep(1)

DISTANCE_FROM_ROBOT = 2.0


class C(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
        return
    
    def get_consumers(self, Consumer, channel):
        return [Consumer( [face_detector_queue, command_queue, move_coordinates_queue], callbacks = [ self.process_face, self.process_command, self.process_move_coordinates ])]
    
    def process_face(self, body, message):
    
        if message.delivery_info['routing_key'] == "face_detector":
            # print message
            
            json_acceptable_string = body.replace('"',"\"")
            body = json.loads(json_acceptable_string)
            print body
            
            current_x = sim.m1.present_position
            current_y = sim.m2.present_position

            x_deg = numpy.rad2deg(numpy.arctan(body['xc']/(320/DISTANCE_FROM_ROBOT)/DISTANCE_FROM_ROBOT))
            y_deg = numpy.rad2deg(numpy.arctan(body['yc']/(240/DISTANCE_FROM_ROBOT)/DISTANCE_FROM_ROBOT))
            print(str(x_deg) + " " + str(y_deg))

            new_pose = {'m1':x_deg,'m2':y_deg}
            sim.goto_position(new_pose,duration=0.5,wait=False)

            # if body['xc'] > 20:
            #   sim.m1.goto_position(sim.m1.present_position-10,duration=1,wait=False)
            # if body['xc'] < -20:
            #   sim.m1.goto_position(sim.m1.present_position+10,duration=1,wait=False)
            message.ack()

    def process_command(self, body, message):
        
        if message.delivery_info['routing_key'] == "command":
            
            if body == "think":
                sim.think_s.start()
                time.sleep(3)

            elif body == "yes":
                sim.yes_s.start()
                time.sleep(3)

            elif body == "no":
                sim.no_s.start()
                time.sleep(3)

            if body == "happy":
                sim.happy_s.start()
                time.sleep(3)

            elif body == "sad":
                sim.sad_s.start()
                time.sleep(3)

            if body == "little happy":
                sim.littlehappy_s.start()
                time.sleep(3)

            elif body == "little sad":
                sim.littlesad_s.start()
                time.sleep(3)

            elif body == "shocked":
                sim.shocked_s.start()
                time.sleep(3)

            elif body == "sleep":
                sim.sleep_s.start()
                time.sleep(3)

            elif body == "wake":
                sim.wake_s.start()
                time.sleep(3)

            elif body == "idle":
                sim.idle.start()
                time.sleep(3)

            elif body == "wake_d":
                sim.wake_d.start()
                time.sleep(3)

            elif body == "sleep_d":
                sim.sleep_d.start()
                time.sleep(3)

            elif body == "think_d":
                sim.think_d.start()
                time.sleep(3)

            elif body == "yes_d":
                sim.yes_d.start()
                time.sleep(3)

            elif body == "no_d":
                sim.no_d.start()
                time.sleep(3)

            elif body == "switch_state":
                sim.switch_state.start()
                time.sleep(3)

            elif body == "experimenter":
                new_pose = {'m1':70, 'm2':0, 'm3':0}
                sim.goto_position(new_pose,duration=random.uniform(0.6,0.8), wait=False)

            elif body == "participant":
                new_pose = {'m1':0, 'm2':0, 'm3':0}
                sim.goto_position(new_pose,duration=random.uniform(0.2,0.5), wait=False)

            elif body == "table":
                new_pose = {'m1':0, 'm2':30, 'm3':0}
                sim.goto_position(new_pose,duration=random.uniform(0.3,0.7), wait=False)

            message.ack()

    def process_move_coordinates(self, body, message):
        
        if message.delivery_info['routing_key'] == "move_coordinates":
             
            print("looking at " + body)

            if body == "experimenter":
                new_pose = {'m1':70, 'm2':0, 'm3':0}
                sim.goto_position(new_pose,duration=random.uniform(0.6,0.8), wait=False)

            elif body == "participant":
                new_pose = {'m1':0, 'm2':0, 'm3':0}
                sim.goto_position(new_pose,duration=random.uniform(0.2,0.5), wait=False)

            elif body == "table":
                new_pose = {'m1':0, 'm2':30, 'm3':0}
                sim.goto_position(new_pose,duration=random.uniform(0.3,0.7), wait=False)



            message.ack()

with Connection('amqp://guest:guest@localhost//') as connection:
    try:
        C(connection).run()
    except KeyboardInterrupt:
        print("Quitting Application")



sim.close()


