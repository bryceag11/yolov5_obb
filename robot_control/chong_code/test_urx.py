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

def connect_to_robot():
    RobotIP = "192.168.1.102"#your PC must have same first 3 components of ip but different last 
    robot = urx.Robot(RobotIP)

    if robot.is_running():
        print("Robot is Online")
        return robot
    else:
        print("Robot is Stopped")
        return 0

def move_to_position(robot, pos, acceleration, speed):
    # Change position slightly
    # robot.translate((0,0.0001,0), acceleration, speed)

    # Move to position
    RobotMovement.movel(pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],acceleration,speed)

def translate_to_position(robot, xyz, acceleration, speed):
    current_pos = robot.getl()
    new_pos = [0, 0, 0]
    for i in range(3):
        xyz[i] = xyz[i]
        new_pos[i] = current_pos[i] + xyz[i]

    RobotMovement.movel(new_pos[0],new_pos[1],new_pos[2],current_pos[3],current_pos[4],current_pos[5],acceleration,speed)

def demo(robot, acceleration, speed):
    # Move slightly
    translate_to_position(robot, [0,0.0001,0], acceleration, speed)
    starting_pos = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, 0, 3.1415926535897932, 0]
    # Open gripper
    RobotMovement.rg_grip(100, 20, 2)
    # Move up in z
    translate_to_position(robot, [0,0,starting_pos[2]], acceleration, speed)
    # Move to xy starting position
    move_to_position(robot, starting_pos, acceleration, speed)
    print("AT STARTING POSITION")
    # Move to xy position and pick up box
    translate_to_position(robot, [-0.2,-0.14,0], acceleration, speed)
    print("MOVED XY")
    translate_to_position(robot, [0,0,-0.22], acceleration, speed)
    print("MOVED Z")
    
    RobotMovement.rg_grip(75, 20, 2)
    print("GRIPPED")
    # Move to different position and drop box
    translate_to_position(robot, [0.1,0.1,0.22], acceleration, speed)
    translate_to_position(robot, [0,0,-0.22], acceleration, speed)
    RobotMovement.rg_grip(100, 20, 2)

    # Go back to starting position
    translate_to_position(robot, [0,0,starting_pos[2]], acceleration, speed)
    move_to_position(robot, starting_pos, acceleration, speed)





    


    

# acceleration = 1
# speed = 0.01


# Starting position
# [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, 0, 3.1415926535897932, 0]
# DEMO CODE
# Put robot into starting position
# pos = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, 0, 3.1415926535897932, 0]

# RobotMovement.rg_grip(100, 20, 2)
# current_pos = robot.getl()
# print(robot.getl())
# current_pos[2] = pos[2]
# Move up in z
# RobotMovement.movel(current_pos[0],current_pos[1],current_pos[2],current_pos[3],current_pos[4],current_pos[5],acceleration,speed)

# Move to position
# RobotMovement.movel(pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],acceleration,speed)
# RobotMovement.rg_grip(100, 20, 2)

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


# RobotMovement.execute(robot)


# robot.translate((0,0.1,0),acceleration,speed)

# DATA RETRIEVAL COMMAND EXAMPLES
# For getl:
#   Compared to the "Base" view on robot:
#   MONITOR: [x,y,z,rx,ry,rz]
#   CODE:    [x,y,z,rx,ry,rz]
#   
#
#   For gripper to be perpendicular to table:
#   _code means the coordinates as input into code
#   rx_code = pi = 3.1415926535897932
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

def turn_gripper(deg):
    if deg == 180:
        coord = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, math.radians(180), 0, 0]
def main():
    robot = connect_to_robot()
    if robot == 0:
        # Error has occured
        return 0
    
    # Determined starting position based off "Base" view on robot
    # demo(robot, 1, 0.02)
    # starting_pos = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, 0, 3.1415926535897932, 0]
    print(robot.getl())

    acceleration = 1
    speed = 0.07

    
    # l_coord = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, math.radians(180), 0, 0]
    # robot.movel(l_coord,acceleration,speed)
    # time.sleep(3)
    # l_coord = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, math.radians(164), math.radians(73), 0]
    # robot.movel(l_coord,acceleration,speed)
    # time.sleep(3)

    # robot.movel(l_coord,acceleration,speed)

    # pos = [-0.647, 0.169, 0.22352142951900683, 1.57, 0, 0]
    # print(robot.getl())
    # pos = [-0.647, 0.169, 0.22352142951900683, 1.57, 0, 0]
    #robot.movel(l_coord,acceleration,speed)
    # move_to_position(robot, starting_pos, acceleration, speed)
    
    # translate_to_position(robot, [0,0,0.01], acceleration, speed)
    # RobotMovement.execute(robot)
    robot.close()

main()