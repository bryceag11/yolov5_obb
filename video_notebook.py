# %%
#Generate .jpgs from .mov
import cv2
vid = cv2.VideoCapture( 'WeldVideo.MOV')
success, image = vid.read()
count = 0
while success:
    cv2.imwrite(f"video_img/{count}.jpg",image)
    success, image = vid.read()
    print('Read a new frame: ', success)
    count += 1

# %%
#generate data needed for video

import pandas as pd
import os
import numpy as np

default_path = os.path.expanduser("~") + r"\OneDrive - University of Kentucky\CIRP\Chosen Control\2021-12-19-14-45-45"
filePath = default_path + "/wd_0.100_0.100_0.100_adam.csv"
inData = pd.read_csv(filePath).to_numpy()
startBuffer = 15
changeBuffer = 30
weldData = np.empty([0,4])

for i in range(startBuffer):
    imgName = default_path+f"/no.bmp"
    weldData = np.vstack((weldData,np.array([imgName,0,inData[0,5],inData[0,8]])))

imgTime = inData[0,1]
imgName = default_path+f"/{imgTime:1.3f}.bmp"
weldData = np.vstack((weldData,np.array([imgName,inData[0,3],inData[0,5],inData[0,8]])))
for i in range(1,357):
    if inData[i,2] == inData[i-1,2]:
        imgTime = inData[i,1]
        imgName = default_path+f"/{imgTime:1.3f}.bmp"
        weldData = np.vstack((weldData,np.array([imgName,inData[i,3],inData[i,5],inData[i,8]])))
    else:
        for j in range(changeBuffer//2):
            imgTime = inData[i-1,1]
            imgName = default_path+f"/{imgTime:1.3f}.bmp"
            weldData = np.vstack((weldData,np.array([imgName,inData[i-1,3],inData[i-1,5],inData[i-1,8]])))
        for k in range(1+changeBuffer-(changeBuffer//2)):       
            imgTime = inData[i,1]
            imgName = default_path+f"/{imgTime:1.3f}.bmp"     
            weldData = np.vstack((weldData,np.array([imgName,inData[i,3],inData[i,5],inData[i,8]])))


video_path = os.path.expanduser("~") + r"\OneDrive - University of Kentucky\CIRP\Video\video_img"
weldInd = np.arange(0,912,4)
vidInd = np.arange(44,728,3)
outData = np.empty([228,5],dtype='<U101')
for i in range(228):
    outData[i,:] = np.append(weldData[weldInd[i]],video_path+f"/{vidInd[i]:d}.jpg") 




# %%
#Generate Video, Square

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\jake229\Dependicies\FFmpeg\bin\ffmpeg.exe'

fname = r'C:\Users\jake229\OneDrive - University of Kentucky\CIRP\Video\weldGraphs.mp4'
fig= plt.figure(figsize=(10,8),constrained_layout=True)
subfigs = fig.subfigures(2,1,height_ratios=[2,3])
vidax = subfigs[0].subplots(1,2)
data_ax = subfigs[1].subplots(3,1)

vidax[0].axis('off')
vidax[1].axis('off')
data_ax[0].set_title("Width (mm)")
data_ax[1].set_title("Current (A)")
data_ax[2].set_title("Speed (mm/s)")
data_ax[0].axes.set_xticks([])
data_ax[1].axes.set_xticks([])
data_ax[0].axes.xaxis.set_ticklabels([])
data_ax[1].axes.xaxis.set_ticklabels([])
data_ax[0].axes.set_xlim([0,15])
data_ax[1].axes.set_xlim([0,15])
data_ax[2].axes.set_xlim([0,15])
data_ax[0].axes.set_ylim([-0.2,7.2])
data_ax[1].axes.set_ylim([133,151])
data_ax[2].axes.set_ylim([0.0029,0.0047])
plt.xlim([0, 15])

metadata = dict(title = "Movie", artist = "JK")
writer = FFMpegWriter(fps=15,metadata=metadata)
xvals = np.arange(0,15.2,(1/15))
width_vals = outData[:,1].astype(float)*0.1
current_vals = outData[:,2].astype(float)
speed_vals = outData[:,3].astype(float)
xlist = []
width_list = []
current_list = []
speed_list = []
width_plot, = data_ax[0].plot([],[])
current_plot, = data_ax[1].plot([],[])
speed_plot, = data_ax[2].plot([],[])

robot_img= cv2.imread(outData[0,4])[0:512,0:672]
pool_img = cv2.imread(outData[0,0])[0:480,0:630]
rob_frame = vidax[0].imshow(robot_img)
pool_frame = vidax[1].imshow(pool_img)

with writer.saving(fig, fname,dpi=500):
    for k in range(228):
        xlist.append(xvals[k])
        width_list.append(width_vals[k])        
        current_list.append(current_vals[k])
        speed_list.append(speed_vals[k])
        robot_img = cv2.imread(outData[k,4])[0:512,0:672]
        pool_img = cv2.imread(outData[k,0])[0:480,0:630]

        rob_frame.set_data(robot_img)
        pool_frame.set_data(pool_img)
        width_plot.set_data(xlist,width_list)
        current_plot.set_data(xlist,current_list)
        speed_plot.set_data(xlist,speed_list)
        writer.grab_frame()



# %%
#Generate Video, Wide

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\jake229\Dependicies\FFmpeg\bin\ffmpeg.exe'

fname = r'C:\Users\jake229\OneDrive - University of Kentucky\CIRP\Video\weldGraphs_wide.mp4'
fig= plt.figure(figsize=(12,5),constrained_layout=True)
subfigs = fig.subfigures(1,2,width_ratios=[2,3])
vidax = subfigs[0].subplots(3,1,gridspec_kw={'height_ratios':[4,.5,4]})
data_ax = subfigs[1].subplots(3,1)

vidax[0].axis('off')
vidax[1].axis('off')
vidax[2].axis('off')
data_ax[0].set_title("Width (mm)")
data_ax[1].set_title("Current (A)")
data_ax[2].set_title("Speed (mm/s)")
data_ax[0].axes.set_xticks([])
data_ax[1].axes.set_xticks([])
data_ax[0].axes.xaxis.set_ticklabels([])
data_ax[1].axes.xaxis.set_ticklabels([])
data_ax[0].axes.set_xlim([0,15])
data_ax[1].axes.set_xlim([0,15])
data_ax[2].axes.set_xlim([0,15])
data_ax[0].axes.set_ylim([-0.2,7.2])
data_ax[1].axes.set_ylim([133,151])
data_ax[2].axes.set_ylim([0.0029,0.0047])
plt.xlim([0, 15])

metadata = dict(title = "Movie", artist = "JK")
writer = FFMpegWriter(fps=15,metadata=metadata)
xvals = np.arange(0,15.2,(1/15))
width_vals = outData[:,1].astype(float)*0.1
current_vals = outData[:,2].astype(float)
speed_vals = outData[:,3].astype(float)
xlist = []
width_list = []
current_list = []
speed_list = []
width_plot, = data_ax[0].plot([],[])
current_plot, = data_ax[1].plot([],[])
speed_plot, = data_ax[2].plot([],[])

robot_img= cv2.imread(outData[0,4])[0:512,0:672]
pool_img = cv2.imread(outData[0,0])[0:480,0:630]
rob_frame = vidax[0].imshow(robot_img)
pool_frame = vidax[2].imshow(pool_img)

with writer.saving(fig, fname,dpi=500):
    for k in range(228):
        xlist.append(xvals[k])
        width_list.append(width_vals[k])        
        current_list.append(current_vals[k])
        speed_list.append(speed_vals[k])
        robot_img = cv2.imread(outData[k,4])[0:512,0:672]
        pool_img = cv2.imread(outData[k,0])[0:480,0:630]

        rob_frame.set_data(robot_img)
        pool_frame.set_data(pool_img)
        width_plot.set_data(xlist,width_list)
        current_plot.set_data(xlist,current_list)
        speed_plot.set_data(xlist,speed_list)
        writer.grab_frame()



