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

import numpy as np
import cv2
import os
import math as m 
import glob
import logging

# Path to folder where captured image will be saved
IMAGE_DESTINATION_PATH = os.getcwd()

class PostProcess():
    def __init__(self, logger):
        self.logger = logger 
        # Initialize constants based on focal length to real world map
        self.SCALE = 900 / 830
        self.LEFT_EDGE = 1225
        self.TOP_EDGE = - 450
        
        # Load calibrated depth image of table alone
        self.depth_table_alone = np.loadtxt('robot_detection/depth_table.csv', delimiter=',')

    def get_rwc(self, depth_img, bb_coords):
        # Take difference of depth_img with box and depth_img with table
        depth_img_subtracted = np.abs(self.depth_table_alone - depth_img)

        # Save csv
        depth_img_substracted_path = self.save_depth_csv(depth_img_subtracted, 'robot_detection/output/depth_img_subtracted')
        self.logger.info(f"Depth image subtracted saved at {depth_img_substracted_path}\n")

        # Initialize box height and rwc array
        real_world_coordinates = []

        counter = 0

        # Obtain height for any number of boxes
        for coords in bb_coords:

            # Crop image using leftmost x, rightmost x, uppermost y, lowermost y
            box_depth_img = self.get_cropped_box_depth_img(depth_img_subtracted, coords)

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
            

            # Convert pixel coordinates to real world coordinates
            temp_rwc = list(self.pixel_conversion(coords))

            # Box height is the average of the array
            height = round((sum(arr) / len(arr)), 3)
            abs_height = 0
            
            # Error calculations and height correction depending on box size
            if temp_rwc[6] >= 175:
                if temp_rwc[6] >= 300:
                    abs_height = 46
                else:
                    abs_height = 42
            else:
                abs_height = 54

            error = abs(round(((height - abs_height) / abs_height), 2))
            if error >= 0.2:
                temp_rwc[2] = abs_height / 1000
            else:
                temp_rwc[2] = height / 1000

            self.logger.info(f"############## Results for BOX_{counter} ##############")
            self.logger.info(f"X Center: {temp_rwc[0]} mm")
            self.logger.info(f"Y Center: {temp_rwc[1]} mm")
            self.logger.info(f"Height: {temp_rwc[2]} mm")
            self.logger.info(f"X Angle: {temp_rwc[3]} rad")
            self.logger.info(f"Y Angle: {temp_rwc[4]} rad")
            self.logger.info(f"Box Length: {temp_rwc[6]} mm")
            self.logger.info(f"Box Area: {temp_rwc[7]} mm^2\n")

            real_world_coordinates.append(temp_rwc)
            counter += 1

        return real_world_coordinates

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

            Range: 0-1080 and 560-1400
            960mm is y center. Anything greater is pos y 
        830 PIXEL RECTANGLE DIMENSIONS:
            X: 900mm
            Y: 900mm
        1920x1080 dimensions:
            X:1150mm->1080 pixels
            Y: 900mm->840 pixels

        EDGE OF TABLE:
            LEFT EDGE: 1340mm from robot 
            RIGHT EDGE: 190mm from robot
            Length: 1150mm
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

        x_coordinates = []
        y_coordinates = []
        for coor in coords:
            x_coordinates.append(self.LEFT_EDGE - (self.SCALE * coor[0]))
            y_coordinates.append(self.TOP_EDGE + (self.SCALE * coor[1]))
        
        # Calculate lengths of edges based on Euclidean distance
        length = max([np.sqrt((x2 - x1)**2 + (y2 - y1)**2) for x1, y1, x2, y2 in zip(x_coordinates, y_coordinates, x_coordinates[1:] + [x_coordinates[0]], y_coordinates[1:] + [y_coordinates[0]])])

        # Calculate orientation angles based on the edges (in radians)
        angles = [np.arctan2((y2 - y1), (x2 - x1)) for x1, y1, x2, y2 in zip(x_coordinates, y_coordinates, x_coordinates[1:] + [x_coordinates[0]], y_coordinates[1:] + [y_coordinates[0]])]
        angles = [np.arctan2((y2 - y1), (x2 - x1)) for x1, y1, x2, y2 in zip(x_coordinates, y_coordinates, x_coordinates[1:] + [x_coordinates[0]], y_coordinates[1:] + [y_coordinates[0]])]

        angle_x = angles[0]
        angle_y = angles[1]

        rob_x, rob_y = self.map_orientation(angle_x, angle_y)

        area = self.calculate_area(x_coordinates, y_coordinates)

        # Calculate center coordinates
        cen_x = ((-1* np.mean(x_coordinates)) / 1000)
        cen_y = ((-1 * np.mean(y_coordinates)) / 1000)

        # Return x_coordinates, y_coordinates, lengths, angles, center_x, and center_y  
        return (cen_x, cen_y, 0.0, rob_x, rob_y, 0.0, length, area)
    
    def calculate_area(self, x_coords, y_coords):

        # Apply the shoelace formula to calculate the area
        area = 0.5 * abs(sum(x_coords[i] * y_coords[i + 1] - x_coords[i + 1] * y_coords[i] for i in range(-1, len(x_coords) - 1)))
        return area
    
    def compare_boxes(self, BOX_L, rwc):
        center_x1, center_y1 = rwc[0], rwc[1]
        center_x2, center_y2 = BOX_L[0], BOX_L[1]
        
        # Coputer Euclidian distance between centroids
        distance = np.sqrt((center_x2 - center_x1)**2 + (center_y2 - center_y1)**2)
        # Return distance 
        return distance 
    

    def map_orientation(self, angle_x, angle_y):
        # Given points for CW relations
        cw_points = {
            'yolo_x': [3.14, 2.8674, 2.661, 2.387, 1.977, 1.777, 1.57],
            'yolo_y': [1.57, 1.3033, 1.101, 0.824, 0.42, 0.2057, 0],
            'robot_x': [3.14, 3.1, 3.08, 2.884, 2.76, 2.557, 2.25],
            'robot_y': [0, -0.3, -0.52, -1.2, -1.46, -1.8, -2.25]
        }
        # Given points for CCW relations
        ccw_points = {
            'yolo_x': [0, 0.2976, 0.4536, 0.80325, 1.1258, 1.395, 1.57],
            'yolo_y': [-1.57, -1.276, -1.121, -0.7702, -0.454, -0.1705, 0],
            'robot_x': [3.14, 3.1, 3.08, 3, 2.76, 2.557, 2.25],
            'robot_y': [0, 0.3, 0.52, 0.85, 1.46, 1.8, 2.25]
        }

        degree = 4

        coeff_x_cw = np.polyfit(cw_points['yolo_x'], cw_points['robot_x'], degree)
        coeff_y_cw = np.polyfit(cw_points['yolo_y'], cw_points['robot_y'], degree)
        coeff_x_ccw = np.polyfit(ccw_points['yolo_x'], ccw_points['robot_x'], degree)
        coeff_y_ccw = np.polyfit(ccw_points['yolo_y'], ccw_points['robot_y'], degree)

        if angle_x >= 1.5:
            if angle_y >= 0:
                coeff_x = coeff_x_cw
                coeff_y = coeff_y_cw
            else:
                coeff_x = coeff_x_ccw
                coeff_y = coeff_y_ccw
        else:
            coeff_x = coeff_x_ccw
            coeff_y = coeff_y_ccw

        result_robot_x = np.polyval(coeff_x, angle_x)
        result_robot_y = np.polyval(coeff_y, angle_y)


        # Print YOLO angles and Robot angles
        # print("\nFor YOLO x = {:f}, Robot x = {:f}".format(angle_x, result_robot_x))
        # print("\nFor YOLO y = {:f}, Robot y = {:f}".format(angle_y, result_robot_y))

        return(result_robot_x, result_robot_y)


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
            self.logger.info("No .txt files found in the folder.")
            return None
        
    def pull_coordinates(self, txt_path):
        pixel_coords_list = []
        with open(txt_path, 'r') as file:
            for line in file:
                values = line.split()

                pixel_coords = [
                (int(float(values[1])), int(float(values[2]))),
                (int(float(values[3])), int(float(values[4]))),
                (int(float(values[5])), int(float(values[6]))), 
                (int(float(values[7])), int(float(values[8])))
                ]

                pixel_coords_list.append(pixel_coords)

        return pixel_coords_list

def main():

    # Perform post processing with cropped images 
    # Change path as needed

    info_handler = logging.FileHandler(filename="robot_detection/runs/post_proc.log")
    info_handler.setLevel(logging.INFO)

    # Define the format for info logs
    info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)

    # Create a logger object
    info_logger = logging.getLogger()
    info_logger.addHandler(info_handler)


    depth_image_path = 'robot_detection/cropped_images/depth/depth_csv216.csv'
    depth_img = np.loadtxt(depth_image_path, delimiter=',')

    post_proc = PostProcess(info_logger)


    sd = "runs\detect\exp239\labels"
    file_path = post_proc.get_txt_path(sd)

    coords = post_proc.pull_coordinates(file_path)
    rwc = post_proc.get_rwc(depth_img, coords) # Return real world coordinates

    areas = post_proc.calculate_area(coords)
    print("Areas:", areas)
    largest_area_index = areas.index(max(areas)) 

    # Separate largest box from the rest to act as a base for stacking 
    BOX_L = rwc[largest_area_index]
    print(f"BOX_{largest_area_index} is the largest box and base for stacking")
    print(f"BOX_{largest_area_index}: {BOX_L}")
    del rwc[largest_area_index]
    
    # Create dictionary for the rest of the boxes and dynamically assign variable names
    box_dict = {}
    print(len(rwc))
    for i in range(len(rwc)):
        x = (rwc[i][0]) * 1000
        y = (rwc[i][1]) * 1000
        if -780 <= x <= -350 and -400 <= y <= 160:
            box_dict[f"BOX_{i}"] = rwc[i]
            print(f"BOX_{i}:", box_dict[f"BOX_{i}"])
        else:
            print(f"BOX_{i} is outside valid range and will be ignored.")



if __name__ == "__main__":
    main()