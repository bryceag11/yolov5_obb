# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 14:47:06 2021

@author: JK
"""
import urx
import numpy as np
import math
import time
from robot_rg import RobotMovement

RobotIP = "192.168.1.102"#your PC must have same first 3 components of ip but different last 
robot = urx.Robot(RobotIP)

if robot.is_running():
    print("Robot is Online")
else:
    print("Robot is Stopped")


acceleration = 1
speed = 0.07

# DEMO CODE
# Put robot into starting position
robot.translate((0,0.0001,0),acceleration,speed)
pos = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, -3.1415926535897932, 0, 0]

RobotMovement.rg_grip(100, 20, 2)
current_pos = robot.getl()
current_pos[2] = pos[2]
# Move up in z
RobotMovement.movel(current_pos[0],current_pos[1],current_pos[2],current_pos[3],current_pos[4],current_pos[5],acceleration,speed)

# Move to position
RobotMovement.movel(pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],acceleration,speed)
RobotMovement.rg_grip(100, 20, 2)

# Move to position and pick up box
# pos[0] = pos[0] - 0.2
# pos[1] = pos[1] - 0.14
# RobotMovement.movel(pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],acceleration,speed)
# pos[2] = pos[2] - 0.22
# RobotMovement.movel(pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],acceleration,speed)
# RobotMovement.rg_grip(75, 20, 2)

# # Move to different position and drop box
# pos[0] = pos[0] + 0.1
# pos[1] = pos[1] + 0.1
# pos[2] = pos[2] + 0.22
# RobotMovement.movel(pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],acceleration,speed)
# pos[2] = pos[2] - 0.22
# RobotMovement.movel(pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],acceleration,speed)
# RobotMovement.rg_grip(100, 20, 2)


RobotMovement.execute(robot)


# robot.translate((0,0.1,0),acceleration,speed)

# DATA RETRIEVAL COMMAND EXAMPLES
# For getl:
#   Compared to the "Base" view on robot:
#   MONITOR: [x,y,z,rx,ry,rz]
#   CODE:    [x,y,z,-rx,-ry,-rz]
#   
#
#   For gripper to be perpendicular to table:
#   _code means the coordinates as input into code
#   rx_code = -pi = -3.1415926535897932
#   ry_code = 0
#   rz_code = 0
#
# print("getl:")
# print(robot.getl())
# print("getj:")
# print(robot.getj())

# MOVE COMMAND EXAMPLES
# robot.translate((0.1,0,0),acceleration,speed)
#j_coord = [-0.05, -1.6802054844298304, 1.7184866110431116, -1.5934087238707484, 4.6951446533203125, -6.211931217704908]
#robot.movej(j_coord,acceleration,speed)
# l_coord = [-0.4550003686706134, -0.08367360368256559, 0.46805276617235847, -2.401674690355295, -2.0140191669171927, -0.04400904500245573]
# robot.movel(l_coord,acceleration,speed)

# GRIPPER EXAMPLES
# Width - How wide the gripper will go
# Force - How fast the gripper moves
# Mass - ???
# width = 105
# force = 20
# mass = 2
# RobotMovement.rg_grip(width, force, mass)
# width = 75
# force = 5
# mass = 2
# RobotMovement.rg_grip(width, force, mass)
# RobotMovement.execute(robot)


robot.close()