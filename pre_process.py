'''
File Name: pre_process.py

Description: This script provides a class for processing obtained images to the camera before deploying yolo model

Usage: For use with the CameraOperation class or with existing images
Create an instance of PreProcess class or run 'python pre_process.py' in terminal
Comment appropriately depending on usage

Output: Saves cropped (and raw) images to directory depending on intended testing mode

Author: Cole Gutterman & Bryce Grant


Purpose: AISM Lab Robotic Automation
'''

import numpy as np
import cv2
from camera_operation import CameraOperation # Uncomment testing portion in main
import os 

IMAGE_DESTINATION_PATH = os.getcwd()

class PreProcess():
    def __init__(self):
        pass

    def crop_images_to_table(self, depth_img, color_img):
        # Zero out anything past the table
        depth_img[depth_img > 1100] = 0

        # Crop images (matches with YOLOv5)
        depth_img = depth_img[125:955, 560:1390]
        depth_img = np.rot90(depth_img)
        color_img = color_img[125:955, 560:1390]
        color_img = cv2.rotate(color_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return depth_img, color_img
    
    '''
    Redundant class methods, repeated for now
    '''
    def save_captured_image(self, image_array, image_name):
        image_path = self.get_unique_file_path(image_name, 'JPEG')
        cv2.imwrite(image_path, image_array)
        return image_path

    def save_depth_csv(self, depth_image, image_name):
        depth_csv_path = self.get_unique_file_path(image_name, 'csv')
        np.savetxt(depth_csv_path, depth_image, delimiter=",")
        return depth_csv_path

    def get_unique_file_path(self, image_name, end):
        # Initialize the counter variable
        counter = 1

        # Iterate until a unique filename is found
        while True:
            depth_csv_name = f'{image_name}{counter}.{end}'
            depth_csv_path = os.path.join(IMAGE_DESTINATION_PATH, depth_csv_name)

            # Check if the file already exists
            if not os.path.exists(depth_csv_path):
                break

            counter += 1
        return depth_csv_path



def main():

    '''
    Testing with CameraOperation class
    '''
    # # Global variables that need to be edited
    # # Path to Azure Kinect bin folder
    # bin_path = r'C:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\bin'
    # # Path to folder where captured image will be saved 
    # image_destination_path = r'C:\Users\bryce\yolov5_obb'

    camera_op = CameraOperation()
    pre_proc = PreProcess()

    depth_img, color_img = camera_op.obtain_images()

    depth_img, color_img = pre_proc.crop_images_to_table(depth_img, color_img)

    depth_csv_path = camera_op.save_depth_csv(depth_img, 'robot_detection/cropped_images/depth/depth_csv')
    print(f"Depth image CSV saved at {depth_csv_path}")

    color_image_path = camera_op.save_captured_image(color_img, 'robot_detection/cropped_images/color/color_image')
    print(f"Color image saved at {color_image_path}")
    
    '''
    End of testing with CameraOperation class
    '''

    '''
    Testing with raw images
    '''
    
    # depth_csv_path = 'robot_detection/raw_images/depth/depth_csv6.csv'
    # color_image_path = 'robot_detection/raw_images/color/color_image6.jpeg'
    # depth_img = np.loadtxt(depth_csv_path, delimiter=',')
    # color_img = cv2.imread(color_image_path)
    # pre_proc = PreProcess()

    # depth_img, color_img = pre_proc.crop_images_to_table(depth_img, color_img)

    
    # depth_csv_path = pre_proc.save_depth_csv(depth_img, 'robot_detection/cropped_images/depth/depth_csv')
    # print(f"Depth image CSV saved at {depth_csv_path}")

    # color_image_path = pre_proc.save_captured_image(color_img, 'robot_detection/cropped_images/color/color_image')
    # print(f"Color image saved at {color_image_path}")

    '''
    End of testing with raw images
    '''


if __name__ == '__main__':
    main()
