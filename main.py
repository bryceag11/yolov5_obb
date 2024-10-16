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
import cv2
import queue

# Bryce path
# sys.path.append('C:/Users/Bryce/yolov5_obb/robot_control/chong_code')
# Lab computer path
sys.path.append(r'C:/Users/AISMLab/Robot_Project/Code/yolov5_obb/robot_control/chong_code')

from test_urx import TestURX

class Detector:
    def __init__(self, post_process_instance, BOX_L, robot, logger):
        self.post_process_instance = post_process_instance
        self.BOX_L = BOX_L
        self.robot = robot
        self.logger = logger

    def run_detection(self, length):
        time.sleep(2)
        for i in range(length):
            self.if_stacked = False
            self.picked_up = False 

            # While loop for box being picked up
            tcp_array = []
            self.logger.info(f"Outputting TCP z force for BOX_{i}")
            while not self.picked_up:
                force = self.robot.get_tcp_force()
                self.logger.info(force[2])
                tcp_array.append(force[2])
                if len(tcp_array) > 1:
                    diff = abs(tcp_array[-1] - tcp_array[-2])
                    if diff > 3:
                        self.logger.info(f"BOX_{i} picked up\n")
                        self.picked_up = True 
                    time.sleep(0.2)

            # While loop for box being stacked
            self.logger.info(f"Outputting distance comparison for BOX_{i}")
            while not self.if_stacked:
                box_coords = self.robot.getl()
                # Compare centroids 
                stacked = self.post_process_instance.compare_boxes(self.BOX_L, box_coords)
                self.logger.info(f"Difference of distance: {stacked}mm")
                tcp_array = []
                # # Determine if distance is below threshold, indicating if boxes are stacked
                if stacked < .030:
                    self.logger.info(f"BOX_{i} in region, outputting TCP force")
                    while not self.if_stacked:
                        force = self.robot.get_tcp_force()
                        self.logger.info(force[2])
                        tcp_array.append(force[2])
                        if len(tcp_array) > 2:
                            diff = tcp_array[-1] - tcp_array[-2]
                            if abs(diff) > 2.5:
                                self.logger.info(f"BOX_{i} stacked\n")
                                self.if_stacked = True
                        time.sleep(0.2)
                time.sleep(0.3)

            time.sleep(4)

        return
    
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


def capture_frames(cap, output_queue, stop_event):
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        output_queue.put(frame)

    # Signal that capturing is done
    output_queue.put(None)

def write_video(output_path, input_queue, width, height, fps):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        frame = input_queue.get()
        if frame is None:  # None indicates end of frames
            break
        out.write(frame)

    out.release()


# Stack boxes function
def main():
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

    # Create class instances
    test_urx = TestURX(logger=info_logger)
    camera_op = CameraOperation()
    pre_proc = PreProcess()
    yolov5 = YOLOV5Detector()
    post_proc = PostProcess(logger=info_logger)

    try:
        info_logger.info("Beginning of log")

        # Move robot to starting position
        try:
            robot = test_urx.connect_to_robot()
            test_urx.move_to_starting_position(1, 0.5)
        except Exception as e:
            info_logger.error(f"Error during robot connection: {e}")
            raise

        try:
            # Create a video writer object for saving the captured video

            info_logger.info("Camera operation beginning...")
            # CAMERA OPERATION
            depth_img, color_img = camera_op.obtain_images()
            info_logger.info("Images captured")

            # Start video capture thread
            cap = cv2.VideoCapture(1)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = 20.0
            output_queue = queue.Queue()
            stop_event = threading.Event()

            capture_thread = threading.Thread(target=capture_frames, args=(cap, output_queue, stop_event))
            write_thread = threading.Thread(target=write_video, args=("captured_video.mp4", output_queue, width, height, fps))

            capture_thread.start()
            write_thread.start()

            # IMAGE PREPROCESSING
            depth_img, color_img = pre_proc.crop_images_to_table(depth_img, color_img)
            info_logger.info("Images cropped")

            depth_csv_path = pre_proc.save_depth_csv(depth_img, 'robot_detection/cropped_images/depth/depth_csv')
            info_logger.info(f"Depth image CSV saved at {depth_csv_path}")

            color_image_path = pre_proc.save_captured_image(color_img, 'robot_detection/cropped_images/color/color_image')
            info_logger.info(f"Color image saved at {color_image_path}\nCamera operation ending...\n")

        except Exception as e:
            info_logger.error(f"Error during image capture: {e}")
            raise           




        # YOLOv5 ORIENTED OBJECT DETECTION
        try: 
            info_logger.info("YOLO inference beginning...")
            opt = yolov5.parse_opt()
            opt.source = color_image_path
            sd = yolov5.run(**vars(opt))
            info_logger.info("YOLO inference ending...\n")
            file_path = post_proc.get_txt_path(sd)
            coords = post_proc.pull_coordinates(file_path) # Pull coordinates from produced yolov5

        except Exception as e:
            info_logger.error(f"Error during YOLO detection: {e}")
            raise # Re-raise 
        
        # POST PROCESSING
        try:
            info_logger.info("Post processing beginning...")
            rwc = post_proc.get_rwc(depth_img, coords) # Return rwc

            # Find largest area index
            largest_area_index = max(range(len(rwc)), key=lambda i: rwc[i][7])

            # Separate largest box from the rest to act as a base for stacking 
            BOX_L = rwc[largest_area_index]
            del rwc[largest_area_index]
            del BOX_L[6:]
            
            info_logger.info(f"BOX_{largest_area_index} is the largest box and base for stacking")

            # Reconfigure rwc to prioritize stacking largest box first
            if any(box[6] > 300 for box in rwc) and (len(rwc) > 1):
                # Sort rwc based on the 7th element of each list
                sorted_rwc = sorted(enumerate(rwc), key=lambda x: x[1][6], reverse=True)
                # Create a new list with updated order
                new_rwc = [box for _, box in sorted_rwc]

                # Now rwc is sorted
                rwc = new_rwc

            # Create dictionary for the rest of the boxes and dynamically assign variable names
            box_dict = {}
            for i in range(len(rwc)):
                x = (rwc[i][0]) * 1000
                y = (rwc[i][1]) * 1000
                if -780 <= x <= -350 and -400 <= y <= 160:
                    box_dict[f"BOX_{i}"] = rwc[i]
                else:
                    info_logger.info(f"BOX_{i} is outside valid range and will be ignored.")
            






        except Exception as e:
            info_logger.error(f"Error during Post Processing: {e}")
            raise 

        if len(box_dict) == 0:
            info_logger.info("Unable to stack boxes due to boxes being absent or out of robot range\n")
            stop_event.set()

            capture_thread.join()
            write_thread.join()

            cap.release()
            time.sleep(5)

        else:
            test_urx.define_box_locations(BOX_L, box_dict)

            # # DYNAMIC DETECTION THREAD
            info_logger.info("Box stacking beginning...")
            # # detector = Detector(post_proc, BOX_L, robot, logger=info_logger)
            # # detection_thread = threading.Thread(target=detector.run_detection, args=(len(box_dict),))
            # # detection_thread.start()
            BOX_L_Neo  = test_urx.pick_up_boxes(1, .4) # Stack boxes first iteration


            stop_event.set()

            capture_thread.join()
            write_thread.join()

            cap.release()

            ########################################################################################
            # SECOND ITERATION of stacking 
            time.sleep(2)
        try:
                
            info_logger.info("Checking for additional boxes added...\n")
            depth_img2, color_img2 = camera_op.obtain_images()
            info_logger.info("Images captured")
            

            cap = cv2.VideoCapture(1)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = 20.0

            output_queue = queue.Queue()
            stop_event = threading.Event()

            capture_thread = threading.Thread(target=capture_frames, args=(cap, output_queue, stop_event))
            write_thread = threading.Thread(target=write_video, args=("captured_video2.mp4", output_queue, width, height, fps))

            capture_thread.start()
            write_thread.start()


            # IMAGE PREPROCESSING
            depth_img2, color_img2 = pre_proc.crop_images_to_table(depth_img2, color_img2)
            info_logger.info("Images cropped")

            depth_csv2_path = pre_proc.save_depth_csv(depth_img2, 'robot_detection/cropped_images/depth/depth_csv')
            info_logger.info(f"Depth image CSV saved at {depth_csv2_path}")

            color_image2_path = pre_proc.save_captured_image(color_img2, 'robot_detection/cropped_images/color/color_image')
            info_logger.info(f"Color image saved at {color_image2_path}\nCamera operation ending...\n")

        except Exception as e:
            info_logger.error(f"Error during image capture: {e}")
            raise
        
        # YOLOv5 ORIENTED OBJECT DETECTION
        try:
            info_logger.info("YOLO inference beginning...")
            opt = yolov5.parse_opt()
            opt.source = color_image2_path
            sd = yolov5.run(**vars(opt))
            info_logger.info("YOLO inference ending...\n")
            file_path = post_proc.get_txt_path(sd)
            coords = post_proc.pull_coordinates(file_path) # Pull coordinates from produced yolov5
        except Exception as e:
            info_logger.error(f"Error during YOLO detection: {e}")
            raise # Re-raise 

        # POST PROCESSING
        try:
            info_logger.info("Post processing beginning...")
            rwc = post_proc.get_rwc(depth_img2, coords) # Return object coordinates in robot coordinate frame
            info_logger.info(f"PREREAL{rwc}")
            # # Calculate areas for each box and return largest area
            # areas = post_proc.calculate_area(coords)
            # info_logger.info("Areas:", areas)
        
            # largest_area_index = areas.index(max(areas)) 
            # if max(areas) >= 35000:
            #     # # Separate largest box from the rest to act as a base for stacking 
            #     BOX_L = [inner_list[largest_area_index] for inner_list in rwc]
            #     info_logger.info(f"BOX{largest_area_index} is the largest box and base for stacking")
            #     for sublist in rwc:
            #         del sublist[largest_area_index]
            # else:
            #     pass
        
            # Reconfigure rwc to remove repeated boxes
            rwc = [box for box in rwc if post_proc.compare_boxes(BOX_L, box) >= .05]
            info_logger.info(f"REAL {rwc}")            # Create dictionary for the rest of the boxes and dynamically assign variable names
            box_dict = {}
            for i in range(len(rwc)):
                x = (rwc[i][0]) * 1000
                y = (rwc[i][1]) * 1000
                if -780 <= x <= -350 and -400 <= y <= 160:
                    box_dict[f"BOX_{i}"] = rwc[i]
                    info_logger.info(f"BOX_{i}:", box_dict[f"BOX_{i}"])
                else:
                    info_logger.info(f"BOX_{i} is outside valid range and will be ignored.")



        except Exception as e:
            info_logger.error(f"Error during Post Processing: {e}")
            raise 
        try:
            if len(box_dict) == 0:
                info_logger.info("Unable to stack boxes due to boxes being absent or out of robot range\n")
                stop_event.set()
                capture_thread.join()
                write_thread.join()
                cap.release()
            else:
                test_urx.define_box_locations(BOX_L_Neo, box_dict)

                # # DYNAMIC DETECTION THREAD
                info_logger.info("Box stacking beginning...")
                # # detector = Detector(post_proc, BOX_L, robot, logger=info_logger)
                # # detection_thread = threading.Thread(target=detector.run_detection, args=(len(box_dict),))
                # # detection_thread.start()
                test_urx.pick_up_boxes(1, 0.4) # Stack boxes first iteration
                stop_event.set()

                capture_thread.join()
                write_thread.join()
                cap.release()
        except KeyboardInterrupt:
            print("\nExiting gracefully....")
            info_logger.info("Keyboard Interrupt.")
            sys.exit(0)
        except Exception as e:
            info_logger.error(f"An unexpected error occurred: {e}")
            raise

    except Exception as e:
        info_logger.error(f"An unexpected error occurred: {e}")
        # Handle other exceptions
        sys.exit(0)

    except KeyboardInterrupt:
        print("\nExiting gracefully....")
        info_logger.info("Keyboard Interrupt.")
        sys.exit(0)

    finally:
        # # Release resources and terminate threads
        if not stop_event.is_set():
            stop_event.set()

        if cap is not None:
            cap.release()  # Release the video capture resource


        # Join threads to wait for their completion
        if capture_thread is not None:
            capture_thread.join()
        if write_thread is not None:
            write_thread.join()


        # Ensure robot connection is closed
        if test_urx is not None:
            test_urx.activate_gripper(100, 20, 2)
            test_urx.close_robot_connection()
            info_logger.info("Robot connection closed.\n")
            info_logger.info('''End of log\n#########################################\n''')
            info_handler.close()
        sys.exit(0)

if __name__ == "__main__":
    main()