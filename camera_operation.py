'''
File Name: camera_operation.py

Description: This script provides a class for controlling the Azure Kinect Camera

Usage: For use with yolov5obb. Create an instance of the 'detection_processing' class or run 'python camera_operation.py'
Saves RGB and depth image to directory

Author: Cole Gutterman & Bryce Grant


Purpose: AISM Lab Robotic Automation
'''
import numpy as np
import cv2
import os
import  pykinect_azure as pykinect

# Global variables
# Path to Azure Kinect bin folder
BIN_PATH = r'C:\Program Files\Azure Kinect SDK v1.4.1\sdk\windows-desktop\amd64\release\bin'
# Path to folder where captured image will be saved 
IMAGE_DESTINATION_PATH = r'C:\Users\bryce\yolov5_obb'

class CameraOperation():
    def __init__(self):
        pass

    def capture_images(self, device, depth_mode, color_resolution):
        ret = False
        while not ret or depth_image.to_numpy()[-1] is None:
            # Attempt to capture image
            capture = device.update()
            ret, depth_image, color_image = self.get_images(capture)

        # Transform depth image to have color image arrangement (spherical to square)
        transformation = pykinect.Transformation(device.get_calibration(depth_mode, color_resolution))
        depth_image = transformation.depth_image_to_color_camera(depth_image)

        return depth_image.to_numpy()[-1], color_image

    def get_images(self, capture):
        # Capture both depth and color image
        depth_image = capture.get_depth_image_object()
        ret, color_image = capture.get_color_image()
        return ret, depth_image, color_image   
    
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
        

    def obtain_images(self):
        # Setup Camera
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
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P  # image quality adjustment

        # Start device
        device = pykinect.start_device(config=device_config)

        # Capture color or depth image from camera
        depth_image, color_image = self.capture_images(device, device_config.depth_mode, device_config.color_resolution)

        # Close Camera
        cv2.destroyAllWindows()
        device.close()
        return depth_image, color_image

# Test Function
def main():

    camera_op = CameraOperation()

    depth_img, color_img = camera_op.obtain_images()

    depth_csv_path = camera_op.save_depth_csv(depth_img, 'robot_detection/raw_images/depth/depth_csv')
    print(f"Depth image CSV saved at {depth_csv_path}")

    color_image_path = camera_op.save_captured_image(color_img, 'robot_detection/raw_images/color/color_image')
    print(f"Color image saved at {color_image_path}")


if __name__ == '__main__':
    main()