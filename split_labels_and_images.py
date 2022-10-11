from glob import glob
from pathlib import Path
import shutil
import os
from tqdm import tqdm


def split_lbl_img(in_folder, out_folder, img_format):
    Path(out_folder, "labels").mkdir(parents=True, exist_ok=True)
    Path(out_folder, "images").mkdir(parents=True, exist_ok=True)

    lbl_files = glob(f"{in_folder}\\obj_train_data\\*.txt")
    img_files = glob(f"{in_folder}\\obj_train_data\\*.{img_format}")

    for lbl_file in tqdm(lbl_files):
        basename=os.path.basename(lbl_file)
        shutil.copyfile(lbl_file, os.path.join(out_folder, "labels", basename))

    for img_file in tqdm(img_files):
        basename=os.path.basename(img_file)
        shutil.copyfile(img_file, os.path.join(out_folder, "images", basename))
    
    shutil.copyfile(f"{in_folder}\\obj.names", f"{out_folder}\\obj.names")


if __name__ == "__main__":
    split_lbl_img("task_сизы 10.06.2022-2022_10_07_14_51_13-yolo 1.1", "dataset2", "png")