# Robotic Project
# 
# find_depth_from_yolo.py
#
# Date: 11/17/2022
#
# Purpose:
#   This code takes the results from YOLOv5 as an input and finds the height of
#   each identified object
#

# General goal:
# 1. Receive input from YOLOv5 on locations of bounding box
# 2. Translate the location to the location in the depth array
# 3. Collect a set amount of depth points in the center of bounding box
# 4. Use algorithm to find an average height
# 5. Return heights for all objects that have a bounding box

# Global variables that need to be edited
# Path to Azure Kinect bin folder
AZURE_KINECT_BIN_PATH  = r'C:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\bin'
# Path to folder where captured image will be saved
IMAGE_DESTINATION_PATH = r'C:\Users\bryce\yolov5_obb'

import numpy as np
import sys
import cv2
import torch
import numpy
import os
from math import floor
import pandas as pd
import detect as yolo

sys.path.append(AZURE_KINECT_BIN_PATH) # Adjust path depending on user looking for "k4a.dll" location
import pykinect_azure as pykinect
from matplotlib import pyplot as plt



def get_obj_height(depth_img, bb_coords):
    # Load calibrated depth image of table alone
    depth_table_alone = np.loadtxt('depth_table.csv', delimiter=',')

    # Take difference of depth_img with box and depth_img with table
    depth_img_subtracted = np.abs(depth_table_alone - depth_img)

    # Save csv
    depth_img_substracted_path = save_depth_csv(depth_img_subtracted, 'depth_img_subtracted')
    print(f"Depth image subtracted saved at {depth_img_substracted_path}")

    # Crop image using leftmost x, rightmost x, uppermost y, lowermost y
    box_depth_img = get_cropped_box_depth_img(depth_img_subtracted, bb_coords)

    # Save cropped depth_img
    box_csv_path = save_depth_csv(box_depth_img, 'box_csv')
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
    print("BOX HEIGHT:")
    print(box_height)
    print("ERROR:")
    print(error)
    return box_height

def get_cropped_box_depth_img(depth_img, bb_coords):
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

def capture_images(device, depth_mode, color_resolution):
    ret = False
    while not ret or depth_image.to_numpy()[-1] is None:
        # Attempt to capture image
        capture = device.update()
        ret, depth_image, color_image = get_images(capture)
    
    # Transform depth image to have color image arrangement (spherical to square)
    transformation = pykinect.Transformation(device.get_calibration(depth_mode, color_resolution))
    depth_image = transformation.depth_image_to_color_camera(depth_image)
    
    return depth_image.to_numpy()[-1], color_image

def get_images(capture):
    # Capture both depth and color image
    depth_image = capture.get_depth_image_object()
    ret, color_image = capture.get_color_image()
    return ret, depth_image, color_image

def save_captured_image(image_array, image_name):
    image_path = get_unique_file_path(image_name, 'JPEG')
    cv2.imwrite(image_path, image_array)
    return image_path

def save_depth_csv(depth_image, image_name):
    depth_csv_path = get_unique_file_path(image_name, 'csv')
    numpy.savetxt(depth_csv_path, depth_image, delimiter=",")
    return depth_csv_path

def get_unique_file_path(image_name, end):
    # Initialize the counter variable
    counter = 1

    # Iterate until a unique filename is found
    while True:
        depth_csv_name = f'{image_name}{counter}.{end}'
        depth_csv_path = os.path.join(IMAGE_DESTINATION_PATH, depth_csv_name)

        # Check if the file already exists
        if (not os.path.exists(depth_csv_path)):
            break

        counter += 1
    return depth_csv_path

def obtain_images():
    ##Setup Camera
    pykinect.initialize_libraries()

    # Modify camera configuration
    device_config = pykinect.default_configuration

    # Depth modes:
    #   - NFOV_2x2Binned
    #   - NFOV_Unbinned 
    #   - WFOV_2x2Binned 
    #   - WFOV_Unbinned 
    #   - Passive IR 
    device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
    device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P #image qualiity adjustment

    # Start device
    device = pykinect.start_device(config=device_config)

    ##Capture color or depth image from camera
    depth_image, color_image = capture_images(device, device_config.depth_mode, device_config.color_resolution)

    ##Close Camera
    cv2.destroyAllWindows()
    device.close()
    return depth_image, color_image

def crop_images_to_table(depth_img, color_img):
    # Zero out anything past the table
    depth_img[depth_img > 1100] = 0

    # Crop images (matches with YOLOv5)
    depth_img = depth_img[125:955, 560:1390]
    color_img = color_img[125:955, 560:1390]
    return depth_img, color_img

def pixel_conversion():
    # Convert the pixels to real world coordinates
    coord = []

def main():
    # Return depth_img array and color_img array
    depth_img, color_img = obtain_images()

    # Edit the image
    depth_img, color_img = crop_images_to_table(depth_img, color_img)

    # Save depth image CSV
    depth_csv_path = save_depth_csv(depth_img, 'depth_csv')
    print(f"Depth image CSV saved at {depth_csv_path}")

    # Save depth image as image (Commented out since it does not help as a JPEG)
    # TODO: Convert to look good as a JPEG
    # cv = ((depth_img - depth_img.min()) / (depth_img.max() - depth_img.min())) * 255
    # depth_img = cv.astype(np.uint8)
    # depth_image_path = save_captured_image(depth_img, 'depth_image')
    # print(f"Depth image saved at {depth_image_path}")

    # Save color image
    color_image_path = save_captured_image(color_img, 'color_image')
    print(f"Color image saved at {color_image_path}")

    print('SUCCESS!')

    ## Run YOLOv5
    opt = yolo.parse_opt()

    yolo.run(**vars(opt))





    ###############################################
    # Dictionary representing the bounding box from YOLOv5
    # This is hardcoded for testing; these will be inputs
    file_path = 'runs\detect\exp25\labels\color_image1.txt' 

    with open(file_path, 'r') as file:
        values = file.readline().split()

    # Initialize the coordinate array
    # Elements of array are tuples with (x,y) coordinates from YOLOv5
    bb_coords = [
        (int(float(values[1])), int(float(values[2]))),
        (int(float(values[3])), int(float(values[4]))),
        (int(float(values[5])), int(float(values[6]))), 
        (int(float(values[7])), int(float(values[8])))
    ]

    get_obj_height(depth_img, bb_coords)

main()