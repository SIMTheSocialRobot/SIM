from pypot.robot.config import ergo_robot_config
import pypot.dynamixel
import pypot.robot
import itertools, numpy, time

AMP = 60
FREQ = 0.5


dxl_io = pypot.dynamixel.DxlIO('/dev/cu.usbmodem14231')
ids = [1,2,3]

speed = dict(zip(ids, itertools.repeat(80)))
dxl_io.set_moving_speed(speed)
pos = dict(zip(ids, itertools.repeat(0)))
dxl_io.set_goal_position(pos)


t0 = time.time()
while True:
    t = time.time()
    if (t - t0) > 5:
        break

    pos = AMP * numpy.sin(2*numpy.pi*FREQ*t)
    dxl_io.set_goal_position(dict(zip(ids, itertools.repeat(pos))))

    time.sleep(0.02)

print(dict(zip(ids, itertools.repeat(pos))))
dxl_io.close()
