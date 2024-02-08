import urx
import numpy as np
import math
import time
import sys
import cv2
import torch
from urx.robotiq_two_finger_gripper import RobotiqScript
from urx.urscript import URScript
import cv2
import torch

sys.path.insert(0, './yolov5')
sys.path.append(r'C:\Users\czh231\Desktop\ResearchFall22\pyKinectAzure-master\pyKinectAzure-master') # Adjust path depending on user
import pykinect_azure as pykinect

class robot_movement():

    #initialize header and output
    file = open(r'D:\Code\yolov5_obb\robot_control\chong_code\Vgripper.script', 'rb')
    header = file.read()
    output = header

    def rg_grip(width, force, mass):      # control the gripper
        force = str(force)
        width = str(width)
        mass = str(mass)

        force = force.encode()
        width = width.encode()
        mass = mass.encode()

        on_return = b"on_return=rg_grip(" + width + b", " + force + b", tool_index = 0, blocking = True, depth_comp = False, popupmsg = True)"
        rg_payload_set = b"rg_payload_set(" + mass + b", tool_index = 0, use_guard = True)"
       
        robot_movement.output = robot_movement.output+ b"\n" + on_return + b"\n" + rg_payload_set + b"\n"          

    def movel(x,y,z,a,b,c,acc,speed):  #a,b,c are angles for gripper
        x = str(x)
        y = str(y)
        z = str(z)
        a = str(a)
        b = str(b)
        c = str(c)
        acc = str(acc)
        speed = str(speed)

        x = x.encode()
        y = y.encode()
        z = z.encode()
        a = a.encode()
        b = b.encode()
        c = c.encode()
        acc = acc.encode()
        speed = speed.encode()
       
        # way_point = b"  global Waypoint_1_p=p["+ x + b", "+ y + b", " + z + b", " + a + b", " + b + b", " + c + b"]"
        movel = b"  movel(" + b"p["+ x + b", "+ y + b", " + z + b", " + a + b", " + b + b", " + c + b"]" +b"," + acc +b", "+ speed + b")"
        # movel = b"  movel(Waypoint_1_p" +b"," + acc +b", "+ speed + b")"
        robot_movement.output = robot_movement.output + b"\n" + movel + b"\n"
       
        # print(output)
 

    def execute(robot):
               
        robot_movement.output = robot_movement.output + b"\nend\n"
        robot_movement.output = robot_movement.output.decode("utf-8")      
        robot.send_program(robot_movement.output)
        # print(robot_movement.output)
        robot_movement.output = b""    

    def vg_release(channel, timeout, autoidle):
        #on return inputs to strings
        channel = str(channel)
        timeout = str(timeout)
        autoidle = str(autoidle)
        #on return encoding
        channel = channel.encode()
        timeout = timeout.encode()
        autoidle = autoidle.encode()
        #which need to be variables and which are constant
        on_return = b"on_return = vg_release(channel = "+ channel + b", timeout = "+ timeout + b", autoidle = "+ autoidle + b", tool_index = 0)"
         #What are the numbers at the begining and do i need to make variables
        vg_payload_set = b"vg_payload_set( 0.0, 2, tool_index =  0 )"
        robot_movement.output = robot_movement.output+ b"\n"+ on_return + b"\n" +  vg_payload_set + b"\n"
           
    def vg_grip(channel, vacuum, timeout, alert, delay, mass):
        #vg_grip_delayed inputs to strings
        channel = str(channel)
        vacuum = str(vacuum)
        timeout = str(timeout)
        alert = str(alert)
        delay = str(delay)
        mass = str(mass)
        #vg_grip_delayed encoding
        channel = channel.encode()
        vacuum = vacuum.encode()
        timeout = timeout.encode()
        alert = alert.encode()
        delay = delay.encode()
        mass = mass.encode()
        #which need to be variables and which are constant
        vg_grip_delayed = b"vg_grip_delayed(tool_index = 0, channel = "+ channel + b", vacuum = "+ vacuum + b", timeout = "+ timeout + b", alert = "+ alert + b", delay = "+ delay + b", mass = "+ mass + b")"
        robot_movement.output = robot_movement.output+ b"\n"+ vg_grip_delayed + b"\n"  
         
       

def coordinates_conversion(X,Y):          # return Xout,Yout
    # polynomial trendline of Order 2
    x = 0.0023*Y**2 - 3.9255*Y + 617.71
    # polynomial trendline of Order 2
    pixel_per_mm = 2E-07*Y**2 + 0.0007*Y + 0.4436
    # centerline coincides with the column where the point (-600,+100) is located
    print(pixel_per_mm)
    y = ((998 - X) / pixel_per_mm) + 100
    return (x+215,y-10)
def live_yolo_with_kincet():               # return pixel coordinate
    sys.path.insert(0, './yolov5')
    sys.path.append(r'C:\Users\czh231\Desktop\ResearchFall22\pyKinectAzure-master\pyKinectAzure-master') # Adjust path depending on user
    import pykinect_azure as pykinect

    if __name__ == "__main__":

        # Model
        #model = torch.hub.load(r'C:\Users\mwda229\Desktop\ResearchFall22', 'best.pt',source='local')
        model = torch.hub.load(r'C:\Users\czh231\Desktop\ResearchFall22', 'custom', path=r'C:\Users\czh231\Desktop\ResearchFall22\best.pt', source='local')  # local repo

        # Initialize the library, if the library is not found, add the library path as argument
        pykinect.initialize_libraries()

        # Modify camera configuration
        device_config = pykinect.default_configuration
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P #image qualiity adjustment
        # print(device_config)

        # Start device
        device = pykinect.start_device(config=device_config)
        img_name = 0
        cv2.namedWindow('Color Image',cv2.WINDOW_NORMAL)

       
        # while True:

            # Get capture
        ret = False
        while not ret:
            capture = device.update()

                # Get the color image from the capture

            ret, color_image = capture.get_color_image()
        # if not ret:
        #     continue
           
            ####################YOLO##################################
       

            # Images
        imgs = [color_image]  # batch of images

            # Inference
        results = model(imgs)
        results.print()
        print('\n',results.xyxy[0]) # x1 (pixels)  y1 (pixels)  x2 (pixels)  y2 (pixels)   confidence        class
        boxResultsTensor = results.xywh[0]  # img1 predictions (tensor) [xmin,ymin,xmax,ymax,class]
        boxResultsPD = results.pandas().xywh[0]  # img1 predictions (pandas) [xmin,ymin,xmax,ymax,class,name]
        boxResultsNP = boxResultsPD.to_numpy()
            # boxResultsList = results.tolist()
       
           
            ####################YOLO##################################
           
   
            # Plot the image
            # box_stream = results.render()[0]
            # cv2.imshow("Color Image",box_stream)
            # cv2.imwrite(f'C:/Users/czh231/Desktop/For Report/ForRecording/{img_name}.JPEG',color_image)
            # Take pictures when ready
        if cv2.waitKey(1) == ord('s'):
            cv2.imwrite(f'C:/Users/czh231/Desktop/For Report/ForRecording/{img_name}.JPEG',color_image) #### Save Image to 'Images' folder ####
        img_name += 1
            # Press q key to stop
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        cv2.destroyAllWindows()

        results.show()  # prints image of classification
        print('Pixel coordinates ready')
        device.close()
    return results
def connect_to_robot():                    # connect and check if robot it's online
    RobotIP = "192.168.1.102"  # must have same first 3 components of ip but different last
    print(urx.__version__)
    robot = urx.Robot(RobotIP)
    if robot.is_running():
        print("Robot is Online")
    else:
        print("Robot is Stopped")
   
    return robot

def compare_boxes(results):             # Compare the size of boxes, and return box1 as bigger one, both in real world coordinates    
    # Extract the first two detections
    box1 = results.xywh[0][0].cpu().numpy()
    box2 = results.xywh[0][1].cpu().numpy()

    # Calculate the area of each box
    area_box1 = box1[2] * box1[3]
    area_box2 = box2[2] * box2[3]

    box11 = box1[0],box1[1]
    box22 = box2[0],box2[1]

    # Compare the areas, Keep box11 always the bigger one
    if area_box1 > area_box2:
        box11 = box1[0],box1[1]
        box22 = box2[0],box2[1]
    elif area_box1 < area_box2:
        box11 = box2[0],box2[1]
        box22 = box1[0],box1[1]
   
    box11=coordinates_conversion(box11[0],box11[1])
    box22=coordinates_conversion(box22[0],box22[1])

    return box11,box22



# #t1=results.xyxy[0]
# t1=results.xyxy[0][0]
# t2=results.xyxy[0][1]
# # Convert tensor2 to list and filter for floating-point numbers
# floats_in_t1 = [x for x in t1.tolist() if isinstance(x, float)]
# del floats_in_t1[-2:]
# print(floats_in_t1)

# floats_in_t2 = [x for x in t2.tolist() if isinstance(x, float)]
# del floats_in_t2[-2:]
# print(floats_in_t2)

# # Get (Xp1,Yp1)
# first_element1 = (floats_in_t1[0] + floats_in_t1[2]) / 2
# second_element1 = (floats_in_t1[1] + floats_in_t1[3]) / 2
# final_p_output1 = [first_element1, second_element1]

# # Get (Xp2,Yp2)
# first_element2 = (floats_in_t2[0] + floats_in_t2[2]) / 2
# second_element2 = (floats_in_t2[1] + floats_in_t2[3]) / 2
# final_p_output2 = [first_element2, second_element2]

# Xout1,Yout1=coordinates_conversion(final_p_output1[0],final_p_output1[1])
# Xout1 = Xout1-40
# Yout1= Yout1+8

# Xout2,Yout2=coordinates_conversion(final_p_output2[0],final_p_output2[1])
# Xout2 = Xout2-40
# Yout2= Yout2+8

# results=live_yolo_with_kincet()

# box11,box22=compare_boxes(results)

# X1=box11[0]*0.001
# Y1=box11[1]*0.001
# X2=box22[0]*0.001
# Y2=box22[1]*0.001
# print(X1,Y1,X2,Y2)
# acc = 0.25
# speed = 0.15

# robot=connect_to_robot()

# L0 = [-0.25, 0.1, 0.21127386450698715, 2.1775829327814487, 2.255375679045388,
#       -0.034366439521176434]
# L1 = [-0.667875741584795, 0.03838465062959279, 0.007271853886109514, 2.1651181179836265, 2.2028379726726928,
#       -0.05855197900615317]
# L2 = [-0.7810098717897483, -0.16262004650176654, 0.15131203740931504, -2.048954734451929, -2.3010953416302726,
#       0.07882830059799721]
# L3 = [-0.801959996584124, -0.15914238811541018, 0.007271853886109514, 2.0982858676376415, 2.2358350769795594,
#       -0.07033327290414629]

# j0 = robot.getj()  # get absolute joint position in radians(each entry corresponds to one joint)
# l0 = robot.getl()  # get xyz(first three digits) and axis-angle vector(last three)

# robot_movement.movel(Xout1,Yout1,0.21,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.rg_grip(105, 5, 2)
# # time.sleep(5) # wait for gripper to fully open

# robot_movement.movel(Xout1,Yout1,0.0072,L1[3],L1[4],L1[5],acc,speed)
# robot_movement.rg_grip(73, 15, 2)
# # time.sleep(5) # wait for gripper to fully close

# robot_movement.movel(Xout1,Yout1,0.21,L1[3],L1[4],L1[5],acc,speed)
# robot_movement.movel(L0[0],L0[1],0.21,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.movel(L0[0],L0[1],0.0005,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.rg_grip(100, 5, 2)
# # time.sleep(5) # wait for gripper to fully open
# robot_movement.movel(L0[0],L0[1],0.21,L0[3],L0[4],L0[5],acc,speed)

# robot_movement.movel(X1,Y1,0.15,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.movel(X1,Y1,-0.13,L1[3],L1[4],L1[5],acc,speed)
# robot_movement.vg_grip(2,30,0.0,"False",0.0,0.0)                # Grip box1

# robot_movement.movel(X1,Y1,0.15,L1[3],L1[4],L1[5],acc,speed)
# robot_movement.movel(L0[0],L0[1],0.15,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.movel(L0[0],L0[1],-0.13,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.vg_release(2, 5.0, "False")                      # Release box1
# robot_movement.movel(L0[0],L0[1],0.15,L1[3],L1[4],L1[5],acc,speed) # back to the sky
# # time.sleep(5) # wait for gripper to fully open

# robot_movement.movel(X2,Y2,0.15,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.movel(X2,Y2,-0.17,L1[3],L1[4],L1[5],acc,speed)
# robot_movement.vg_grip(2,30,0.0,"False",0.0,0.0)                ## Grip box2


# robot_movement.movel(L0[0],L0[1],0.15,L0[3],L0[4],L0[5],acc,speed)
# robot_movement.movel(L0[0],L0[1],-0.1,L0[3],L0[4],L0[5],acc,speed) ############ Need adjustment on Z
# robot_movement.vg_release(2, 5.0, "False")                      ## Release box2
# robot_movement.movel(L0[0],L0[1],0.15,L1[3],L1[4],L1[5],acc,speed) # back to the sky

# robot_movement.execute(robot)

# time.sleep(5)
# robot.close()