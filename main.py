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

def main():

    # Create class instances
    camera_op = CameraOperation()
    pre_proc = PreProcess()
    yolov5 = YOLOV5Detector()
    post_proc = PostProcess()

    # Image capture
    depth_img, color_img = camera_op.obtain_images()
    print('Images captured \n')

    # Image preprocessing
    depth_img, color_img = pre_proc.crop_images_to_table(depth_img, color_img)
    print('Images cropped \n')

    depth_csv_path = pre_proc.save_depth_csv(depth_img, 'robot_detection/cropped_images/depth/depth_csv')
    print(f"Depth image CSV saved at {depth_csv_path}")

    color_image_path = pre_proc.save_captured_image(color_img, 'robot_detection/cropped_images/color/color_image')
    print(f"Color image saved at {color_image_path}")



    # YOLOv5 Object Detection
    opt = yolov5.parse_opt()
    opt.source = color_image_path
    
    sd = yolov5.run(**vars(opt))

    # Image postprocessing

    file_path = post_proc.get_txt_path(sd)

    coords = post_proc.pull_coordinates(file_path) # Pull coordinates from produced yolov5

    post_proc.get_obj_height(depth_img, coords) # Return object height

    post_proc.pixel_conversion(coords) # Return real world coordinates


if __name__ == "__main__":
    main()