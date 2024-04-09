# -*- coding: utf-8 -*-
import urx
import time
from robot_rg import RobotMovement 

class TestURX:
    def __init__(self):
        # HARDCODED STARTING POSITION
        self.STARTING_POSITION = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, 3.1415926535897932, 0, 0]
        self.BOX_L = None
        self.BOX_DICT = None
        self.HB_0 = None
        self.HB_1 = None
        self.robot = None
        self.box_lists = {}
        self.HB_dict = {}

    def define_box_locations(self, BOX_L, BOX_DICT):
        # HARDCODED STARTING POSITION
        self.STARTING_POSITION = [-0.3855075887632609, -0.08245739447612332, 0.22352142951900683, 3.1415926535897932, 0, 0]
        self.BOX_L = BOX_L
        self.BOX_DICT = BOX_DICT
        # self.HB_0 = self.BOX_0[2]
        # self.HB_1 = self.BOX_1[2]
        # Parse box_dict into lists for each box and assign HB... to the respective height
        for i, box_key in enumerate(BOX_DICT.keys()):
            box_coords = BOX_DICT[box_key]
            self.HB_dict[f"HB_{i}"] = box_coords[2] # Assign height to HB_dict key
            box_coords[2] *= 2

    def connect_to_robot(self):
        RobotIP = "192.168.1.102"  # Your PC must have same first 3 components of IP but different last
        self.robot = urx.Robot(RobotIP)

        if self.robot.is_running():
            print("Robot is Online")
            return self.robot
        else:
            print("Robot is Stopped")

    def activate_gripper(self, width, force, mass):
        print("ACTIVATE GRIPPER")
        ag = RobotMovement()
        ag.rg_grip(self.robot, width, force, mass)
        time.sleep(0.5)
        # print(self.robot.is_program_running())
        while self.robot.is_program_running():
            time.sleep(0.5)
            # print(self.robot.is_program_running())

    def move_to_starting_position(self, acceleration, speed):
        # Move slightly
        self.robot.translate((0,0.000001,0), acceleration, speed)
        # Move to starting position
        print("MOVE TO STARTING POSITION")
        self.robot.movel(self.STARTING_POSITION, acceleration, speed)
        self.activate_gripper(100, 20, 2)

    def pick_up_boxes(self, acceleration, speed):
        # time.sleep(5)
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
        for i in range(len(self.BOX_DICT)):
            self.robot.movel(self.BOX_DICT[f'BOX_{i}'], acceleration, speed)
            self.robot.translate((0,0, -1.5*(self.HB_dict[f"HB_{i}"])), acceleration, speed)
            # time.sleep(5)
            self.activate_gripper(75, 20, 2)
            # time.sleep(5)
            self.BOX_L[2] += self.HB_dict[f"HB_{i}"]
            self.robot.translate((0, 0, (self.BOX_L[2])), acceleration, speed)
            self.robot.movel(self.BOX_L, acceleration, speed)
            self.robot.translate((0, 0, -(self.HB_dict[f"HB_{i}"]/2)), acceleration, speed)
            # time.sleep(5)
            # robot.translate((0,0, -.0225), acceleration, speed)
            # time.sleep(5)
            self.activate_gripper(100, 20, 2)
            self.robot.translate((0, 0, (self.HB_dict[f"HB_{i}"])), acceleration, speed)
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

    def demo(self, acceleration, speed):
        self.move_to_starting_position(acceleration, speed)
        self.robot.translate((-0.1,-0.1,-0.1), acceleration, speed)
        self.activate_gripper(75, 20, 2)
        self.robot.translate((0.1,0.1,0.1), acceleration, speed)
        self.activate_gripper(100, 20, 2)

    def close_robot_connection(self):
        if self.robot is not None:
            self.robot.close()

def main():
    test_urx = TestURX()
    test_urx.connect_to_robot()
    test_urx.move_to_starting_position(1, 0.08)
    # test_urx.demo(1, 0.08)
    test_urx.close_robot_connection()

if __name__ == '__main__':
    main()
