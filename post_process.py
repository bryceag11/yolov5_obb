'''
File Name: depth_detect.py

Description: This script provides a class for processing bounding box information from YOLO to find the height and dimensions of the bpxes

Usage: For use with yolov5obb. Create an instance of the 'detection_processing' class

Author: Cole Gutterman & Bryce Grant


Purpose: AISM Lab Robotic Automation
'''


# Global variables that need to be edited
# Path to Azure Kinect bin folder
AZURE_KINECT_BIN_PATH  = r'C:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\bin'
# Path to folder where captured image will be saved
IMAGE_DESTINATION_PATH = r'C:\Users\bryce\yolov5_obb'

import numpy as np
import cv2
import os
import math as m 
import glob

class PostProcess():
    def __init__(self):
        pass

    def get_obj_height(self, depth_img, bb_coords):
        # Load calibrated depth image of table alone
        depth_table_alone = np.loadtxt('robot_detection/depth_table.csv', delimiter=',')

        # Take difference of depth_img with box and depth_img with table
        depth_img_subtracted = np.abs(depth_table_alone - depth_img)

        # Save csv
        depth_img_substracted_path = self.save_depth_csv(depth_img_subtracted, 'robot_detection/output/depth_img_subtracted')
        print(f"Depth image subtracted saved at {depth_img_substracted_path}")

        # Crop image using leftmost x, rightmost x, uppermost y, lowermost y
        box_depth_img = self.get_cropped_box_depth_img(depth_img_subtracted, bb_coords)

        # Save cropped depth_img
        box_csv_path = self.save_depth_csv(box_depth_img, 'robot_detection/output/box_csv')
        print(f"Box image CSV saved at {box_csv_path}")

        # Find center x and y of box csv
        x = np.shape(box_depth_img)[0] - 1
        y = np.shape(box_depth_img)[1] - 1
        center_x = round(x / 2)
        center_y = round(y / 2)

        # Put center and surrounding points into array
        # Note: The indices of the loop can be changed to add more or less
        # points around the center of the box to be a part of average
        arr = []
        for i in range(-3,4):
            for j in range(-3,4):
                arr.append(box_depth_img[center_x + i][center_y + j])
        
        # Box height is the average of the array
        box_height = round((sum(arr) / len(arr)), 3)

        # Display stats
        error = abs(round(((box_height - 54) / 54), 2))
        print("\nBOX HEIGHT:")
        print(box_height)
        print("\nERROR:")
        print(error)
        return box_height

    def get_cropped_box_depth_img(self, depth_img, bb_coords):
        # Separate x and y coordinates and put them in arrays
        x_coordinates = []
        y_coordinates = []
        for coords in bb_coords:
            x_coordinates.append(coords[0])
            y_coordinates.append(coords[1])
        
        # Sort each array
        x_coordinates.sort()
        y_coordinates.sort()

        # Determine min and max columns and rows by taking first and last elements
        # in each sorted array
        min_column = x_coordinates[0]
        max_column = x_coordinates[len(x_coordinates) - 1]
        min_row = y_coordinates[0]
        max_row = y_coordinates[len(y_coordinates) - 1]

        # Return cropped image around box
        return depth_img[min_row:max_row, min_column:max_column]

    # Convert the pixels to real world coordinates
    def pixel_conversion(self, coords):

        '''
        TABLE DIMENSIONS: 
            X: 1485mm
            Y: 900mm

        830 PIXEL RECTANGLE DIMENSIONS:
            X: 900mm
            Y: 900mm

        EDGE OF TABLE:
            LEFT EDGE: 155mm from table
            1200mm from robot center
            RIGHT EDGE: 435mm from table
            322.5mm from robot center
        
        ROBOT ZERO COORDINATES:
            X: 112.5mm from right table
            322.5mm from right rectangle edge
            Y: 450mm from top of table
            Also 450mm from zero-y coordinate of rectangle

        RECTANGLE (0,0) REAL COORDINATES:
            X: (+) 1200mm
            Y: (-) 450mm 
        

        Scale: 1.08433735
        Offset:
        '''

        # Set conversion constants based on table dimensions
        SCALE = 900 / 830
        LEFT_EDGE = 1225
        TOP_EDGE = - 450
        

        x_coordinates = []
        y_coordinates = []

        for coords in coords:
            x_coordinates.append(LEFT_EDGE - (SCALE * coords[0]))
            y_coordinates.append(TOP_EDGE + (SCALE * coords[1]))

        length_1 = m.sqrt((x_coordinates[1] - x_coordinates[0])**2 + (y_coordinates[1] - y_coordinates[0])**2)
        length_2 = m.sqrt((x_coordinates[2] - x_coordinates[1])**2 + (y_coordinates[2] - y_coordinates[1])**2)
        print(f"\nLength 1: {length_1}mm | Length 2: {length_2}mm")


        return (x_coordinates, y_coordinates)

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

    def get_txt_path(self, sd):
        txt_files = glob.glob(os.path.join(sd, '*.txt'))

        if txt_files:
            selected_txt = txt_files[0]
            return selected_txt
        else:
            print("No .txt files found in the folder.")
            return None
        
    def pull_coordinates(self, txt_path):
        with open(txt_path, 'r') as file:
            values = file.readline().split()
        # # Assign values to dictionary keys
        
        pixel_coords = [
        (int(float(values[1])), int(float(values[2]))),
        (int(float(values[3])), int(float(values[4]))),
        (int(float(values[5])), int(float(values[6]))), 
        (int(float(values[7])), int(float(values[8])))
         ]
        
        return pixel_coords

def main():

    # Perform post processing with cropped images 
    # Change path as needed
    depth_image_path = 'robot_detection/cropped_images/depth/depth_csv2.csv'
    depth_img = np.loadtxt(depth_image_path, delimiter=',')

    post_proc = PostProcess()


    sd = "runs\detect\exp35\labels"
    file_path = post_proc.get_txt_path(sd)

    coords = post_proc.pull_coordinates(file_path)

    post_proc.get_obj_height(depth_img, coords)

    real_world = post_proc.pixel_conversion(coords)


    print("\nX Coordinates: ", real_world[0])
    print("\nY Coordinates: ", real_world[1])


# if __name__ == "__main__":
#     main()