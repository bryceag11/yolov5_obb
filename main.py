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
import os 
import logging
import datetime

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
        self.picked_up = False 

    def run_detection(self, length):
        for i in range(length):
            self.if_stacked = False
            self.picked_up = False 
            # While loop for box being picked up
            while not self.picked_up:
                force = self.robot.get_tcp_force()
                print(force)
                tcp_array.append(force[2])
                if len(tcp_array) > 1:
                    diff = tcp_array[-1] - tcp_array[-2]
                    print(diff)
                    if abs(diff) > 3:
                        print("Box picked up")
                        self.picked_up = True 
                    time.sleep(0.5)
            
            # While loop for box being stacked
            while not self.if_stacked:
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
                tcp_array = []
                # print(f"\n Difference of Distance: {stacked}mm")
                # # Determine if distance is below threshold, indicating if boxes are stacked
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
                        time.sleep(0.5)
                time.sleep(0.5)

# Function to generate a unique log file name
def generate_log_file_name():
    now = datetime.datetime.now()
    date_str = now.strftime("%d_%m_%Y")
    counter = 1
    log_file_name = f"robot_info_{date_str}_{counter}.log"
    while os.path.exists(log_file_name):
        counter += 1
        log_file_name = f"robot_info_{date_str}_{counter}.log"
    return log_file_name


# Stack boxes function
def main():
    # Create class instances
    test_urx = TestURX()
    camera_op = CameraOperation()
    pre_proc = PreProcess()
    yolov5 = YOLOV5Detector()
    post_proc = PostProcess()

    try:
        # Log file configuration
        log_file_name = generate_log_file_name()
        # Set up logging configuration
        info_handler = logging.FileHandler(filename=f"robot_detection/runs/{log_file_name}")
        info_handler.setLevel(logging.INFO)

        # Define the format for info logs
        info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        info_handler.setFormatter(info_formatter)

        # Create a logger object
        info_logger = logging.getLogger()
        info_logger.addHandler(info_handler)
        
        # Move robot to starting position
        robot = test_urx.connect_to_robot()
        test_urx.move_to_starting_position(1, 0.08)
        try:
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

        except Exception as e:
            info_logger.error(f"Error during image capture or preprocessing: {e}")
            raise # Handle exception at higher level



        # YOLOv5 ORIENTED OBJECT DETECTION
        try: 
            opt = yolov5.parse_opt()
            opt.source = color_image_path
            sd = yolov5.run(**vars(opt))
            file_path = post_proc.get_txt_path(sd)
            coords = post_proc.pull_coordinates(file_path) # Pull coordinates from produced yolov5

        except Exception as e:
            info_logger.error(f"Error during YOLO detection: {e}")
            raise # Re-raise 
        
        # POST PROCESSING
        try:
            height = post_proc.get_obj_height(depth_img, coords) # Return object height
            rwc = list(post_proc.pixel_conversion(coords, height)) # Return real world coordinates
            
            # Calculate areas for each box and return largest area
            areas = post_proc.calculate_area(coords)
            print("\nAreas:", areas)
            largest_area_index = areas.index(max(areas)) 

            # Separate largest box from the rest to act as a base for stacking 
            BOX_L = [inner_list[largest_area_index] for inner_list in rwc]
            print(f"LARGE: {BOX_L}\n")
            for sublist in rwc:
                del sublist[largest_area_index]
            
            # Create dictionary for the rest of the boxes and dynamically assign variable names
            box_dict = {}
            for i in range(len(rwc[0])):
                box_dict[f"BOX_{i}"] = [inner_list[i] for inner_list in rwc]
                print(f"BOX_{i}:", box_dict[f"BOX_{i}"])

        except Exception as e:
            info_logger.error(f"Error during Post Processing: {e}")
            raise 

        test_urx.define_box_locations(BOX_L, box_dict)

        detector = Detector(post_proc, BOX_L, robot)
        detection_thread = threading.Thread(target=detector.run_detection(len(box_dict)))
        detection_thread.start()
        
        test_urx.pick_up_boxes(1, 0.08)

    except Exception as e:
        info_logger.error(f"An unexpected error occurred: {e}")
        # Handle other exceptions
        raise

    except KeyboardInterrupt:
        print("\nExiting gracefully....")
        info_logger.info("Keyboard Interrupt.")

    finally:
        # Ensure robot connection is closed
        test_urx.close_robot_connection()
        info_logger.info("Robot connection closed.")
        info_handler.close()

if __name__ == "__main__":
    main()