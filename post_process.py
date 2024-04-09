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

# Path to folder where captured image will be saved
IMAGE_DESTINATION_PATH = os.getcwd()

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

        # Initialize box height
        box_height = []
        
        counter = 0

        # Obtain height for any number of boxes
        for coords in bb_coords:
            # print(f"\n############## Results for BOX{counter} ##############")

            # Crop image using leftmost x, rightmost x, uppermost y, lowermost y
            box_depth_img = self.get_cropped_box_depth_img(depth_img_subtracted, coords)

        #     # # Save cropped depth_img
        #     # box_csv_path = self.save_depth_csv(box_depth_img, 'robot_detection/output/box_csv')
        #     # print(f"Box image CSV saved at {box_csv_path}")

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
            height = round((sum(arr) / len(arr)), 3)
            box_height.append(height/1000)
            # Display stats
            error = abs(round(((height - 54) / 54), 2))
            # print(f"BOX{counter} HEIGHT:")
            # print(height)
            print(f"\nERROR for BOX{counter} Height:{error}")
            # print(error)

            counter += 1

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
    def pixel_conversion(self, coords, height):

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
        SCALE = 900 / 830
        LEFT_EDGE = 1225
        TOP_EDGE = - 450
        
        center_x = []
        center_y = []
        ang_x = []
        ang_y = []
        ang_z = []
        counter = 0
        for coord in coords:
            print(f"\n############## Results for BOX{counter} ##############")
            x_coordinates = []
            y_coordinates = []

            for coor in coord:
                x_coordinates.append(LEFT_EDGE - (SCALE * coor[0]))
                y_coordinates.append(TOP_EDGE + (SCALE * coor[1]))

            # Calculate lengths of edges based on Euclidean distance
            # lengths = [np.sqrt((x2 - x1)**2 + (y2 - y1)**2) for x1, y1, x2, y2 in zip(x_coordinates, y_coordinates, x_coordinates[1:] + [x_coordinates[0]], y_coordinates[1:] + [y_coordinates[0]])]

            # print(f"Edge Lengths for BOX{counter}:", lengths)

            # Calculate orientation angles based on the edges (in radians)
            angles = [np.arctan2((y2 - y1), (x2 - x1)) for x1, y1, x2, y2 in zip(x_coordinates, y_coordinates, x_coordinates[1:] + [x_coordinates[0]], y_coordinates[1:] + [y_coordinates[0]])]
            
            angle_x = angles[0]
            angle_y = angles[1]

            rob_x, rob_y = self.map_orientation(angle_x, angle_y)

            print(f"X angle for BOX{counter}: {rob_x} rad")
            print(f"Y angle for BOX{counter}: {rob_y} rad")

            # Calculate center coordinates
            cen_x = -1* (np.mean(x_coordinates))
            cen_y = np.mean(y_coordinates)
            print(f"X Center for BOX{counter}: {cen_x} mm")
            print(f"Y Center for BOX{counter}: {-1 * cen_y} mm")
            print(f"Z (Height) for BOX{counter}: {(1000 * height[counter])} mm")
            # Add to the list
            center_x.append(cen_x/1000)
            center_y.append((cen_y/1000)*-1)
            ang_x.append(rob_x)
            ang_y.append(rob_y)
            ang_z.append(0.0)
            counter += 1

        # Return x_coordinates, y_coordinates, lengths, angles, center_x, and center_y  
        return (center_x, center_y, height, ang_x, ang_y, ang_z)
    
    def calculate_area(self, bb_coords):
        areas = []
        for coords in bb_coords:
            # Extract x and y coordinates of the bounding box vertices
            x_coords = [coord[0] for coord in coords]
            y_coords = [coord[1] for coord in coords]

            # Apply the shoelace formula to calculate the area
            area = 0.5 * abs(sum(x_coords[i] * y_coords[i + 1] - x_coords[i + 1] * y_coords[i] for i in range(-1, len(x_coords) - 1)))
            areas.append(area)
        return areas
    
    def compare_boxes(self, box1_coords, box2_coords):
        center_x1, center_y1 = box1_coords[0], box1_coords[1]
        center_x2, center_y2 = box2_coords[0], box2_coords[1]
        
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
            print("No .txt files found in the folder.")
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
    depth_image_path = 'robot_detection/cropped_images/depth/depth_csv46.csv'
    depth_img = np.loadtxt(depth_image_path, delimiter=',')

    post_proc = PostProcess()


    sd = "runs\detect\exp75\labels\color_image46.txt"
    # file_path = post_proc.get_txt_path(sd)

    coords = post_proc.pull_coordinates(sd)
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
    largest_box_coords = rwc[largest_area_index]

    # Separate the largest box from the rest
    largest_box_dict = {"BOX_L": largest_box_coords}
    del box_dict[f"box_{largest_area_index}"]

    # Print the largest box coordinates
    print("Box with largest area:", largest_box_coords)

    # Print the rest of the boxes
    print("Other boxes:")
    for key, value in box_dict.items():
        print(f"{key}: {value}")
                    


if __name__ == "__main__":
    main()