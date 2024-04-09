'''
File Name: main.py

Description: This script is used as the main program for detecting boxes and determining their dimensions in real space

Usage: run 'python main.py'

Author: Cole Gutterman & Bryce Grant

Purpose: AISM Lab Robotic Automation

'''



from pre_process import PreProcess
from yolo_detect import YOLOV5Detector
from camera_operation import CameraOperation
from post_process import PostProcess

import sys
import numpy as np
import math
import time
import threading

# Bryce path
# sys.path.append('C:/Users/Bryce/yolov5_obb/robot_control/chong_code')
# Lab computer path
sys.path.append(r'C:/Users/AISMLab/Robot_Project/Code/yolov5_obb/robot_control/chong_code')

from test_urx import TestURX

class Detector:
    def __init__(self, post_process_instance, BOX_L, robot):
        self.post_process_instance = post_process_instance
        self.BOX_L = BOX_L
        self.robot = robot
        self.if_stacked = False 

    def run_detection(self):

        while True:
            # # Capture images from camera
            # depth_img, color_img = camera_op.obtain_images()
    
            # # Preprocess images
            # depth_img, color_img = pre_proc.crop_images_to_table(depth_img, color_img)

            # # Save color image for YOLO detection (adjust path as needed)
            # color_image_path = pre_proc.save_captured_image(color_img, 'robot_detection/cropped_images/color/color_image')

            # # Run YOLOv5 detection
            # opt = yolov5.parse_opt()
            # opt.source = color_image_path
            # sd = yolov5.run(**vars(opt))
    
            # # Get bounding box coordinates from YOLO results
            # file_path = post_process_instance.get_txt_path(sd)
            # box_coords_list = post_process_instance.pull_coordinates(file_path)
    
            # Assuming you want to compare the first two boxes:

            # box1_coords = box_coords_list[0]

            # box2_coords = box_coords_list[1]

            box_coords = self.robot.getl()
            # Compare centroids 
            stacked = self.post_process_instance.compare_boxes(self.BOX_L, box_coords)

            print(f"\n Difference of Distance: {stacked}mm")
            # Determine if distance is below threshold, indicating if boxes are stacked
            if stacked < 30:
                print("Box in region")
                tcp_array = []
                while True:
                    force = self.robot.get_tcp_force()
                    print(force)
                    tcp_array.append(force[2])
                    if len(tcp_array) > 1:
                        diff = tcp_array[-1] - tcp_array[-2]
                        if abs(diff) > 2:
                            print("Box stacked")
                            self.stacked = True
                            return False
                    time.sleep(0.5)
            time.sleep(0.5)


def main():
    # Move robot to starting position
    test_urx = TestURX()
    test_urx.connect_to_robot()
    test_urx.move_to_starting_position(1, 0.08)

    # Create class instances
    camera_op = CameraOperation()
    pre_proc = PreProcess()
    yolov5 = YOLOV5Detector()
    post_proc = PostProcess()

    # CAMERA OPERATION
    depth_img, color_img = camera_op.obtain_images()
    print('Images captured \n')

    # IMAGE PREPROCESSING
    depth_img, color_img = pre_proc.crop_images_to_table(depth_img, color_img)
    print('Images cropped \n')

    depth_csv_path = pre_proc.save_depth_csv(depth_img, 'robot_detection/cropped_images/depth/depth_csv')
    print(f"Depth image CSV saved at {depth_csv_path}")

    color_image_path = pre_proc.save_captured_image(color_img, 'robot_detection/cropped_images/color/color_image')
    print(f"Color image saved at {color_image_path}")

    # YOLOv5 ORIENTED OBJECT DETECTION
    opt = yolov5.parse_opt()
    opt.source = color_image_path
    
    sd = yolov5.run(**vars(opt))

    
    # POST PROCESSING
    file_path = post_proc.get_txt_path(sd)

    coords = post_proc.pull_coordinates(file_path) # Pull coordinates from produced yolov5

    height = post_proc.get_obj_height(depth_img, coords) # Return object height

    rwc = post_proc.pixel_conversion(coords, height) # Return real world coordinates

    # Calculate areas for each box
    areas = post_proc.calculate_area(coords)
    print("Areas:", areas)
    
    largest_area_index = areas.index(max(areas))
    # Reorder the bounding box coordinates so that the box with the largest area is first


    box_dict = {}
    for i in range(len(rwc[0])):
        box_dict[f"box_{i}"] = [inner_list[i] for inner_list in rwc]
        print(f"BOX {i}:", box_dict[f"box_{i}"])
    
    # Retrieve the box with the largest area
    largest_area_index = areas.index(max(areas))
    largest_box_coords = box_dict[f"box_{largest_area_index}"]
    # Separate the largest box from the rest
    del box_dict[f"box_{largest_area_index}"]
    
    print(largest_box_coords)


    # # Print the rest of the boxes
    print("Other boxes:")
    for key, value in box_dict.items():
        print(f"{key}: {value}")
    # Retrieve the box with the largest area

    test_urx.define_box_locations(largest_box_coords, box_dict)
    # detector = Detector(post_proc, largest_box_coords, robot)
    # detection_thread = threading.Thread(target=detector.run_detection)
    test_urx.pick_up_boxes(1, 0.08)
    # detection_thread.start()
    test_urx.close_robot_connection()

if __name__ == "__main__":
    main()