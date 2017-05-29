from pypot.robot.config import ergo_robot_config
import pypot.dynamixel
import pypot.robot
import itertools, numpy, time
import csv



dxl_io = pypot.dynamixel.DxlIO('/dev/cu.usbmodem1421')
ids = [1,2,3]

speed = dict(zip(ids, itertools.repeat(100)))
dxl_io.set_moving_speed(speed)
pos = {1:20,2:20,3:20}
dxl_io.set_goal_position(pos)
time.sleep(1)

pos = {1:0,2:0,3:0}
dxl_io.set_goal_position(pos)
time.sleep(1)

dxl_io.close()
