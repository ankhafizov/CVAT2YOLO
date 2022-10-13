import argparse
from split_labels_and_images import split_lbl_img
from create_yolov5_dataset import split_class_dir_ratio
import shutil


TEMP_FOLDER = "TEMP"


def main():
    parser = argparse.ArgumentParser(description='Converts CVAT YOLO 1.1 to COCO format')
    parser.add_argument('--CVAT', dest='CVAT_input_folder', required=True,
                        help='path to the root folder of imported from CVAT YOLO 1.1 dataset')
    parser.add_argument('--img_format', dest='img_format', required=True,
                        help='Format of images')
    parser.add_argument('--split', dest='split', type=float, required=True,
                        help="A percentage of a split, e.g. 0.9 means split 0.9 for train and 0.1 for test")
    parser.add_argument('--seed', dest='seed', type=int, default=1227,
                        help="A random seed for reproducebiliry")
    parser.add_argument('--output_folder', dest='output_folder', required=True,
                        help="path to converted dataset folder {root}{dataset name}")

    args = parser.parse_args()

    # ------------------ ARG parse ------------------
    CVAT_input_folder = args.CVAT_input_folder
    img_format = args.img_format
    split = args.split
    seed = args.seed
    output_folder = args.output_folder
    # -----------------------------------------------
    
    # --------------------- main --------------------
    assert ("." not in img_format), "img_format must be without ."
    split_lbl_img(CVAT_input_folder, TEMP_FOLDER, img_format)

    images_dir = f"{TEMP_FOLDER}/images"
    labels_dir = f"{TEMP_FOLDER}/labels"
    split_class_dir_ratio(TEMP_FOLDER, images_dir, labels_dir, output_folder, (split, 1-split), seed, img_format)
    # -----------------------------------------------

    shutil.rmtree(TEMP_FOLDER)

if __name__ == "__main__":
    main()
