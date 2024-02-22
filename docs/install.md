# Windows Installation
## Requirements
* Windows
* Python 3.9+ 
* PyTorch ≥ 2.0.1+cu117, Torchvision ≥ 0.15.2+cu117, Torchaudio ≥ 2.0.2+cu117
* CUDA 11.7 or higher

I have tested the following versions of OS and softwares：
* OS：Windows 11
* CUDA: 11.7, 11.8

## Install 
**CUDA Driver Version ≥ CUDA Toolkit Version(runtime version) = torch.version.cuda**

a. Install CUDA from the [Nvidia website](https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11)

b. Make sure your CUDA runtime api version ≤ CUDA driver version. (for example 11.8 ≤ 12.2)
```
nvcc -V
nvidia-smi
```
c. Install PyTorch and torchvision following the [official instructions](https://pytorch.org/get-started/previous-versions/), Make sure cudatoolkit version same as CUDA runtime api version, e.g.,
```
pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118
nvcc -V
python
>>> import torch
>>> torch.__version__
>>> torch.version.cuda
>>> exit()
```
d. Clone the yolov5-obb repository.
```
git clone https://github.com/bryceag1/yolov5_obb.git
cd yolov5_obb
```
e. Install yolov5-obb requirements.

```
pip install -r requirements.txt
```

## Install DOTA_devkit. 
**(Custom Install, it's just a tool to split the high resolution image and evaluation the obb)**

```
cd yolov5_obb/DOTA_devkit
sudo apt-get install swig
swig -c++ -python polyiou.i
python setup.py build_ext --inplace
```

