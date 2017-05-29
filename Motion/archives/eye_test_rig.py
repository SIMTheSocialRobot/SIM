from pypot.robot.config import ergo_robot_config
import pypot.dynamixel
import pypot.robot
import itertools, numpy, time
import csv



dxl_io = pypot.dynamixel.DxlIO('/dev/cu.usbmodem14231')
ids = [1,2,3]

speed = dict(zip(ids, itertools.repeat(100)))
dxl_io.set_moving_speed(speed)
pos = {1:0,2:-45,3:0}
dxl_io.set_goal_position(pos)


time.sleep(1)

with open('eye_rig_test.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)  # skip the headers
    last_x = 45
    last_y = 45
    for row in reader:
                
        # self.robot.m1.goal_position = int(float(row[1]))
        # self.robot.m2.goal_position = int(float(row[2]))
        current_x = int(float(row[2]))
        current_y = -int(float(row[1]))
        t_int = 0.03
        dxl_io.set_moving_speed({3:(current_x-last_x)/t_int,2:(current_y-last_y)/t_int})
        dxl_io.set_goal_position({3:current_x,2: current_y})
        time.sleep(t_int)
        last_x = int(float(row[2]))
        last_y = int(float(row[1]))



dxl_io.close()
