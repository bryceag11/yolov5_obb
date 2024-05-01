This file houses all of the experiments run through YOLO whether that be training, validation or inference. 

# Location for training results of models proposed within the paper
#### The opt.yaml file may have a different name for the cfg, that is because the OBB was added onto the original yaml file names to match the report notation
- The AISM original trained model was trained with the [yolov5s-OBB-orig.yaml](../models/yolov5s-OBB-orig.yaml) configuration on an older dataset. It can be found under ['runs/train/exp93'](train/exp93). 
- The Finetuned trained model was trained with the [yolov5s-OBB-orig.yaml](../models/yolov5s-OBB-orig.yaml) on FINAL_BOX. It can be found under ['train/exp158'](train/exp158).
- The C3TR trained model was trained with the [yolov5s-OBB-C3TR.yaml](../models/yolov5s-OBB-C3TR.yaml) on FINAL_BOX. It can be found under ['train/exp156'](train/exp156).
- The C3TRGhost trained model was trained with the [yolov5s-OBB-C3TRGhost.yaml](../models/yolov5s-OBB-C3TRGhost.yaml) on FINAL_BOX. It can be found under ['train/exp159'](train/exp159).
- The C3STR trained model was trained with the [yolov5s-OBB-C3STR.yaml](../models/yolov5s-OBB-C3STR.yaml) on FINAL_BOX. It can be found under ['train/exp151'](train/exp151).
- The C3STRGhost trained model was trained with the [yolov5s-OBB-C3STRGhost.yaml](../models/yolov5s-OBB-C3STRGhost.yaml) on FINAL_BOX. It can be found under [train/exp155'](train/exp155).
