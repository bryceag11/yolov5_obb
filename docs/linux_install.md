# YOLOV5 OBB Linux Installation Instructions 
## Requirements
* Linux, (Ubuntu 22.04 demonstrated)*
* Python 3.9+ 
* PyTorch ≥ 2.0.1+cu117, Torchvision ≥ 0.15.2+cu117, Torchaudio ≥ 2.0.2+cu117
* CUDA 11.7 or higher

I have tested the following versions of OS and softwares：
* OS：Ubuntu 20.04/22.04
* CUDA: 11.7/11.8

## Ubuntu Setup
To run ‘yolov5_obb’ you must have a linux distribution installed. 
The easiest way to do this is to install Ubuntu 22.04 which runs the kernel through a virtual machine.
You can install Ubuntu 22.04 by going to the windows store and searching for ‘Ubuntu 22.04’ seen in the pictures below 

![Microsoft Store](https://github.com/bryceag11/yolov5_obb/assets/67086260/2277a2d2-3ba1-480a-ae0a-53de9df963fd)

![Ubuntu 22.04](https://github.com/bryceag11/yolov5_obb/assets/67086260/c5fc9dc1-bd84-46df-9ba6-b8f7e9048f04)

Once this is done, Ubuntu will be installed on the device and then programs can be ran in Visual Studio or at the Ubuntu terminal.

![image](https://github.com/bryceag11/yolov5_obb/assets/67086260/cbbfc92f-5601-4a9b-93de-f3c0be8da94a)

![image](https://github.com/bryceag11/yolov5_obb/assets/67086260/6babc8dc-fa81-4bc4-8f21-05ca498c6c4a)

Run the following commands:
* Update the Ubuntu package repository using the following command:
``` sudo apt-get update ```
* Install the build-essential package:
``` sudo apt-get install software-properties-common ```
* Use the following command to check the GCC version: ``` gcc--version ```



## Python Setup

This section starts with modifying our python version. To begin, run the following commands. 
a. Add the Personal Package Archive (PPA) repo
 ```
 sudo add-apt-repository ppa:deadsnakes/ppa
 ```
b. Update Ubuntu repo
 ```
 sudo apt-get update
 ```
c. Install python 3.9:
 ```
 sudo apt-get install python3.9
 ```
d. Update your update-alternatives:
```
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 2
```
 
e. Set your default python version (Python 3.9):
```
sudo update-alternatives --set python /usr/bin/python3.6
```
f. Run 'python' to verify it was installed correctly
g.  Transfer pip data to computer and install distutils to build packages
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo apt install python3.9-distutils
```
h. Install pip
```
python3.9 get-pip.py
```
## CUDA & PyTorch Installation

For yolov5_obb we will be using CUDA V11.7. You will be training models on your GPU through using CUDA on the Linux shell. Therefore, we must install CUDA through Ubuntu.
Review the bash file 'cuda_install_instr.sh' within the GitHub and install it to your Linux system. Run the script to install CUDA successfully.
```
bash cuda_install_instr.sh
```
![Cuda Instructions](https://github.com/bryceag11/yolov5_obb/assets/67086260/bd75b53f-bdd4-410d-b14b-66b5ac0a53d6)

Once complete, run 'nvcc -V' within the terminal to check the CUDA driver version. This simultaneously verifies a correct CUDA installation.

![Nvidia Driver Check](https://github.com/bryceag11/yolov5_obb/assets/67086260/7da60f82-ac79-4fbe-999f-7f833bb6cdf1)

Since this script installs torch as well, run the commands below to verify the torch installation. Ensure your output matches the figure below EXACTLY.
```
python
import torch, torchaudio, torchvision
torch.__version__
torchaudio.__version__
torchvision.__version__
```

![image](https://github.com/bryceag11/yolov5_obb/assets/67086260/20936d1f-205a-433d-8ac9-f3309c237e0f)

## Project Installation

Clone the repository on your machine: ``` git clone https://github.com/bryceag11/yolov5_obb.git ```

Once you are in the folder, run ``` pip install -r requirements.txt ``` to install all the dependencies (python modules). \

Next, setup the environment.
```
cd utils/nms_rotated
pip install -v -e .  #or "pip install -v -e ."
```
Once you have done this, you are officially ready to train using yolov5_obb.


