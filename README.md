# CVAT2YOLO Converter

Converter CVAT dataset to YOLOv5 format

# Installation

`git clone https://github.com/ankhafizov/CVAT2YOLO.git`

`cd CVAT2YOLO`

`pip install -e .` 

# Usage

Example

`cvat2yolo --CVAT "my datset" --img_format png --split 0.9 --output_folder "out/my_dataset_yolov5"`

where kwargs:

- --CVAT - Path to the root folder of imported from CVAT YOLO 1.1 dataset
- --img_format - Format of images
- --split - A percentage of a split, e.g. 0.9 means split 0.9 for train and 0.1 for test
- --output_folder - Path to converted dataset folder {root}{dataset name}
- --percentage_empty - Percentage of images without any labels in relation to full dataset size (default =10, optional)

help:

`cvat2yolo --h` or `cvat2yolo -h` 