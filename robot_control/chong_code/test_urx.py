# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 14:47:06 2021

@author: JK
"""
import urx
import numpy as np
import math
import time
from robot_rg import robot_movement

rm = robot_movement()

RobotIP = "192.168.1.102"#your PC must have same first 3 components of ip but different last 
robot = urx.Robot(RobotIP)

if robot.is_running():
    print("Robot is Online")
else:
    print("Robot is Stopped")


acceleration = 1
speed = 0.05


print("getl:")
print(robot.getl())
print("getj:")
print(robot.getj())

# robot.translate((-0.1,0,0),acceleration,speed)

# note the "rob" object being passed here
# gripper = URRoboRobotiq_Two_Finger_Gripper()
# gripper.close_gripper()

#j_coord = [-0.05, -1.6802054844298304, 1.7184866110431116, -1.5934087238707484, 4.6951446533203125, -6.211931217704908]
#robot.movej(j_coord,acceleration,speed)
# l_coord = [-0.4550003686706134, -0.08367360368256559, 0.46805276617235847, -2.401674690355295, -2.0140191669171927, -0.04400904500245573]
# robot.movel(l_coord,acceleration,speed)
# robot.movej(j75,acceleration,speed)

robot.close()