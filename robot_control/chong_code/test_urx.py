# -*- coding: utf-8 -*-
"""
File Name: test_urx.py

Description: This script is used as the test program to move the robot and gripper to interact with the environment
Values corresponding to the box orientation and position in the robot coordinate frame are passed into this program (hard-coded as of now)
Usage: 

Author: Cole Gutterman & Bryce Grant

Purpose: AISM Lab Robotic Automation
"""
import urx
import numpy as np
import math
import time
from robot_rg import RobotMovement
 

# HARDCODED STARTING POSITION
STARTING_POSITION = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, 3.1415926535897932, 0, 0]
BOX_0 = [-0.5608433734939758, -0.3171686746987951, 0.061939, 3.1338287888130534, 0.0694892875624884, 0.0]
BOX_1 = [-0.7403012048192771, -0.07536144578313253, 0.088653, 2.2487423090771657, -2.2589397740851616, 0.0]
HB_0 = BOX_0[2]
HB_1 = BOX_1[2]
BOX_1[2] += .025
def connect_to_robot():
    RobotIP = "192.168.1.102"#your PC must have same first 3 components of ip but different last
    robot = urx.Robot(RobotIP)
 
    if robot.is_running():
        print("Robot is Online")
        return robot
    else:
        print("Robot is Stopped")
        return 0
 
def activate_gripper(robot, width, force, mass):
    ag = RobotMovement()
    ag.rg_grip(robot, width, force, mass)
    print(robot.is_program_running())
    while robot.is_program_running():
        print(robot.is_program_running())
        time.sleep(5)
    return
 
# def open_gripper(robot, width, force, mass):
#     activate_gripper(robot, width, force, mass)
 
#     return
 
# def close_gripper(robot, width, force, mass):
#     activate_gripper(robot, width, force, mass)
 
#     return
 
def demo(robot, acceleration, speed):
    # Move slightly
    robot.translate((0,0.000001,0), acceleration, speed)
 
    # Move to starting position
    print("MOVE TO STARTING POSITION")
    robot.movel(STARTING_POSITION, acceleration, speed)
   
    # Open gripper
    # print("OPEN GRIPPER")
    # activate_gripper(robot, 100, 20, 2)
    # time.sleep(5)
    # print("TRANSLATE")
    # Move to xy position and pick up box
    # robot.translate((-0.1,-0.1,0), acceleration, speed)
    # robot.translate((0, 0, -0.22), acceleration, speed)
 
    '''
    Stack boxes
   
    '''
 
    # Initialize with open gripper
    # time.sleep(5)
    # activate_gripper(robot, 100, 20, 2)
    # time.sleep(5)
 
    robot.movel(BOX_0, acceleration, speed)
    robot.translate((0,0, -(HB_0+.005)), acceleration, speed)
    time.sleep(5)
    activate_gripper(robot, 100, 20, 2)
    time.sleep(5)
    activate_gripper(robot, 75, 20, 2)
    time.sleep(5)
    robot.translate((0,0, (HB_0)), acceleration, speed)
    robot.movel(BOX_1, acceleration, speed)
    time.sleep(5)
    # robot.translate((0,0, -.0225), acceleration, speed)
    # time.sleep(5)
    # activate_gripper(robot, 100, 20, 2)
    # time.sleep(5)    
    # time.sleep(5)
    # activate_gripper(robot, 100, 20, 2)
    # time.sleep(5)
 
    # # # Close gripper
    # # print("ACTIVATE GRIPPER")
    # # activate_gripper(robot, 75, 20, 2)
 
    # # # print("TRANSLATE")
    # # # Move to different position and drop box
    # robot.translate((0.1,0.1,0.22), acceleration, speed)
    # robot.translate((0,0,-0.22), acceleration, speed)
    # activate_gripper(robot, 100, 20, 2)
 
    # # Go back to starting position
    # pos = robot.getl()
    # robot.movel((pos[0],pos[1],STARTING_POSITION[2],pos[3],pos[4],pos[5]), acceleration, speed)
    # robot.movel(STARTING_POSITION, acceleration, speed)
 
def main():
    robot = connect_to_robot()
    if robot == 0:
        # Error has occured
        return 0
    # demo(robot, 1, .08)

    robot.translate((0,0,-0.22), 1, 0.08)
    # # demo(robot, 1, 0.08)
    # time.sleep(5)
 
    # activate_gripper(robot, 75, 20, 2)
    # time.sleep(5)
    # activate_gripper(robot, 100, 20, 2)
    # time.sleep(5)
    # activate_gripper(robot, 75, 20, 2)
    # time.sleep(5)
    # activate_gripper(robot, 100, 20, 2)
    # time.sleep(5)
 
    robot.close()
 
if __name__ == '__main__':
    main()