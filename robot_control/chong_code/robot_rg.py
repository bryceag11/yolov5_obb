import urx
import numpy as np
import math
import time
import sys
import cv2
import torch
from urx.robotiq_two_finger_gripper import RobotiqScript
from urx.urscript import URScript
import cv2
import torch
 
class RobotMovement():
    def __init__(self):
        #initialize header and self.output
        self.file = open(r'C:\Users\AISMLab\Robot_Project\Code\yolov5_obb\robot_control\chong_code\Rgripper.script', 'rb')
        header = self.file.read()
        self.output = header
 
    def rg_grip(self, robot, width, force, mass):      # control the gripper
        # file = open(r'C:\Users\AISMLab\Robot_Project\Code\yolov5_obb\robot_control\chong_code\Rgripper.script', 'rb')
        # header = file.read()
        # self.output = header
 
        force = str(force)
        width = str(width)
        mass = str(mass)
 
        force = force.encode()
        width = width.encode()
        mass = mass.encode()
 
        on_return = b"on_return=rg_grip(" + width + b", " + force + b", tool_index = 0, blocking = True, depth_comp = False, popupmsg = true)"
        rg_payload_set = b"rg_payload_set(" + mass + b", tool_index = 0, use_guard = True)"
        self.output = self.output+ b"\n" + on_return + b"\n" + rg_payload_set + b"\n"        
        self.output = self.output + b"\nend\n"
        self.output = self.output.decode("utf-8")      
        robot.send_program(self.output)
        self.output = b""  
        self.file.close()
 
    def movel(self, x,y,z,a,b,c,acc,speed):  #a,b,c are angles for gripper
        x = str(x)
        y = str(y)
        z = str(z)
        a = str(a)
        b = str(b)
        c = str(c)
        acc = str(acc)
        speed = str(speed)
 
        x = x.encode()
        y = y.encode()
        z = z.encode()
        a = a.encode()
        b = b.encode()
        c = c.encode()
        acc = acc.encode()
        speed = speed.encode()
       
        # way_point = b"  global Waypoint_1_p=p["+ x + b", "+ y + b", " + z + b", " + a + b", " + b + b", " + c + b"]"
        movel = b"  movel(" + b"p["+ x + b", "+ y + b", " + z + b", " + a + b", " + b + b", " + c + b"]" +b"," + acc +b", "+ speed + b")"
        # movel = b"  movel(Waypoint_1_p" +b"," + acc +b", "+ speed + b")"
        self.output = self.output + b"\n" + movel + b"\n"
       
        # print(self.output)
 
 
    def execute(self, robot):
               
        self.output = self.output + b"\nend\n"
        self.output = self.output.decode("utf-8")      
        robot.send_program(self.output)
        # print(RobotMovement.self.output)
        self.output = b""    
 
    def vg_release(self, channel, timeout, autoidle):
        #on return inputs to strings
        channel = str(channel)
        timeout = str(timeout)
        autoidle = str(autoidle)
        #on return encoding
        channel = channel.encode()
        timeout = timeout.encode()
        autoidle = autoidle.encode()
        #which need to be variables and which are constant
        on_return = b"on_return = vg_release(channel = "+ channel + b", timeout = "+ timeout + b", autoidle = "+ autoidle + b", tool_index = 0)"
         #What are the numbers at the begining and do i need to make variables
        vg_payload_set = b"vg_payload_set( 0.0, 2, tool_index =  0 )"
        self.output = self.output+ b"\n"+ on_return + b"\n" +  vg_payload_set + b"\n"
           
    def vg_grip(self, channel, vacuum, timeout, alert, delay, mass):
        #vg_grip_delayed inputs to strings
        channel = str(channel)
        vacuum = str(vacuum)
        timeout = str(timeout)
        alert = str(alert)
        delay = str(delay)
        mass = str(mass)
        #vg_grip_delayed encoding
        channel = channel.encode()
        vacuum = vacuum.encode()
        timeout = timeout.encode()
        alert = alert.encode()
        delay = delay.encode()
        mass = mass.encode()
        #which need to be variables and which are constant
        vg_grip_delayed = b"vg_grip_delayed(tool_index = 0, channel = "+ channel + b", vacuum = "+ vacuum + b", timeout = "+ timeout + b", alert = "+ alert + b", delay = "+ delay + b", mass = "+ mass + b")"
        self.output = self.output+ b"\n"+ vg_grip_delayed + b"\n"  
 