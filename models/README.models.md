# An overview of the files contained within this folder and their respective changes are included below. 


## Common.py
Algorithms used for the various layers used within YOLOV5

### Changes made and Usage
- Added the C3STR class, or a C3 module with the Swin Transformer block
- Added the SwinTransformerBlock Class
- Added an Improved Receptive Field Block method (not used within the project)
- Added a Coordinate Attention mechanism (not used within the project)


## Experimental.py
Experimental modules used within YOLOv5 such as Ensemble and MixConv2D

## SwinTransformer.py
Defines a Swin Transformer based on the paper https://arxiv.org/abs/2103.14030

References code developed at https://github.com/anonymoussss/YOLOX-SwinTransformer/blob/master/yolox/models/swin_transformer.py

## tf.py
Tensor flow implementation of common.py

## .yaml files 
Defines the architecture configurations for Yolov5. The names of the files correspond to the various model configurations that we developed. The backbone of the model 
- The AISM original trained model was trained with the [yolov5s-OBB-orig.yaml](yolov5s-OBB-orig.yaml) configuration on an older dataset. It can be found under ['runs/train/exp93'](../runs/train/exp93). 
- The Finetuned trained model was trained with the [yolov5s-OBB-orig.yaml](yolov5s-OBB-orig.yaml) on FINAL_BOX. It can be found under ['runs/train/exp158'](../runs/train/exp158).
- The C3TR trained model was trained with the [yolov5s-OBB-C3TR.yaml](yolov5s-OBB-C3TR.yaml) on FINAL_BOX. It can be found under ['runs/train/exp156'](../runs/train/exp156).
- The C3TRGhost trained model was trained with the [yolov5s-OBB-C3TRGhost.yaml](yolov5s-OBB-C3TRGhost.yaml) on FINAL_BOX. It can be found under ['runs/train/exp159'](../runs/train/exp159).
- The C3STR trained model was trained with the [yolov5s-OBB-C3STR.yaml](yolov5s-OBB-C3STR.yaml) on FINAL_BOX. It can be found under ['runs/train/exp151'](../runs/train/exp151).
- The C3STRGhost trained model was trained with the [yolov5s-OBB-C3STRGhost.yaml](yolov5s-OBB-C3STRGhost.yaml) on FINAL_BOX. It can be found under ['runs/train/exp155'](../runs/train/exp155).

Defines the architecture configurations for Yolov5. The names of the files correspond to the various model configurations that we developed. The backbone of the model 


