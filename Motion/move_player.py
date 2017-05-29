import pypot.robot
import time
import random
import itertools, numpy
import subprocess
import threading
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

from move_player_primitives import SleepPrimitive, CenterPrimitive, CustomPrimitive

media_exchange = Exchange('media', 'direct', durable=True)

eye_control_queue = Queue('eye_control', exchange=media_exchange, routing_key='eye_control')

sim = pypot.robot.from_json('sim_config.json')

sim.attach_primitive(SleepPrimitive(sim,amp=1), 'sleep')
sim.attach_primitive(CenterPrimitive(sim,amp=0.3), 'center')
sim.attach_primitive(CustomPrimitive(sim, file="happy_s02"), 'custom_primitive')


# sim.center.start()
# time.sleep(1)

sim.custom_primitive.start()
time.sleep(3)

sim.close()