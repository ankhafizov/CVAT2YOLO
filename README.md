# CVAT2YOLO Converter

Converter cvat dataset YOLO1.1 to YOLO format (compatible with YOLOv5 and higher models)

---

For a Russian-speaking audience, the tutorial video for this repository is available at the link - [YouTube Video](https://www.youtube.com/watch?v=bw95ipoyHnk)



# Installation

`git clone https://github.com/ankhafizov/CVAT2YOLO.git`

`cd CVAT2YOLO`

`pip install -e .` 

# Usage

1. If val and train parts splitted manually, folders train_folder and val_folder has to exist in cvat dataset folder:

```
cvat2yolo --cvat my_datset --mode manual --train_folder obj_Train_data --val_folder obj_Validation_data  --test_folder obj_Test_data --img_format jpg --output_folder my_dataset_yolov5
```

or more simplified (by default val_folder=obj_Validation_data, train_folder=my_obj_Train_data, test_folder=obj_Test_data, img_format=png will be taken):

```
cvat2yolo --cvat my_datset --mode manual --output_folder my_dataset_yolov5
```

if any of train, val or test folder does not exist, there will not be created corresponding folders in the output directory.

<p align="center">
    =====
</p>

2. In automatic mode ("autosplit") val and train folders would be merged and randomly splitted with the certain proportion:

```
cvat2yolo --cvat my_datset \
          --mode autosplit \
          --split 0.9 \
          --train_folder obj_Train_data \
          --val_folder obj_Validation_data \ 
          --test_folder obj_Test_data \ 
          --img_format png \
          --output_folder out/my_dataset_yolov5
```

or simlified:

```
cvat2yolo --cvat my_datset --mode autosplit --split 0.9 --output_folder out/my_dataset_yolov5
```


# Help:

- --cvat - Path to the root folder of imported from cvat YOLO 1.1 dataset
- --mode - "autosplit" or "manual" (as it was exported from cvat, check the text above)
- --output_folder - Path to converted dataset folder {root}{dataset name}

- --split - A percentage of a split, e.g. 0.9 means split 0.9 for train and 0.1 for test (default None)
- --train_folder - Folder with Train subset inside cvat path (default obj_Train_data)
- --val_folder - Folder with Val subset inside cvat path (default obj_Validation_data)
- --test_folder - Folder with Test subset inside cvat path (default obj_Test_data)
- --img_format - File format of images (default png)
- --label_tfrms - Label union with another one existed in dataset (example: 'head->hood,helmet->hat' will unite
'head' with 'hood' and 'helmet' with 'hat' resulting 'hood' and 'hat' in output dataset)

- --percentage_empty - Allowed percentage of images without any labels in relation to full dataset size (default = 100, optional)
- --classes - Classes which labels to keep. So if in initiall dataset there are 3 classes (e.g. [A, B, C]), and there is flag ```--classes "A|C"```, only labels with classes A and C will be kept in output YOLOv5 dataset.

help:

```
cvat2yolo --help
```


---

## Converting Photos to the Same File Extension:

If your dataset, which you exported from CVAT, contains images with different extensions, you need to first convert all the photos to a fixed format (e.g., png or jpg). Having photos with the same extension is mandatory for the cvat2yolo converter to work.

So, first, you need to go into the make_same_extensions.py file in the repository and specify the folders where you need to change the extensions of the images. Next, you need to install the pillow library (for this, you need to run the command ```pip install pillow``` in the terminal).

Then, you need to run the code to change the extensions by running this command in the terminal: ```python make_same_extensions.py```

After all the folders containing images are converted to the same extensions, you can run the cvat2yolo code (ps: an alternative to running ```cvat2yolo``` may be to run the code in the terminal using the command ```python main_cvat2yolo.py```).