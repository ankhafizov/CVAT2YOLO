import os

from glob import glob
from pathlib import Path
import shutil

from tqdm import tqdm

from lib_utils import is_txt_file_empty


def get_file_paths_lists_for_subset(subset_folder_pth, img_extention, lbl_extention):
    img_file_pths = []
    lbl_file_pths = []

    if os.path.exists(subset_folder_pth):
        img_file_pths.extend(glob(f"{subset_folder_pth}/*.{img_extention}"))

    lbl_file_pths.extend(
        [p.replace(f".{img_extention}", f".{lbl_extention}") for p in img_file_pths]
    )

    return list(zip(img_file_pths, lbl_file_pths))


def manualsplit(
    out_folder,
    train_folder_pth,
    val_folder_pth,
    test_folder_pth,
    img_extention,
    percentage_empty,
    lbl_extention="txt",
):

    img_lbl_file_pth_train = get_file_paths_lists_for_subset(
        train_folder_pth, img_extention, lbl_extention
    )
    img_lbl_file_pth_val = get_file_paths_lists_for_subset(
        val_folder_pth, img_extention, lbl_extention
    )
    img_lbl_file_pth_test = get_file_paths_lists_for_subset(
        test_folder_pth, img_extention, lbl_extention
    )

    print("Creating train dataset")
    N_files_train = len(img_lbl_file_pth_train)
    acceptable_N_of_empty_files = int(N_files_train * percentage_empty / 100)
    count_of_empty_files = 0
    for img, lbl in tqdm(img_lbl_file_pth_train):
        if is_txt_file_empty(lbl):
            count_of_empty_files += 1
            if count_of_empty_files > acceptable_N_of_empty_files:
                continue

        shutil.copy(
            lbl, os.path.join(out_folder, "labels", "train", os.path.basename(lbl))
        )
        shutil.copy(
            img, os.path.join(out_folder, "images", "train", os.path.basename(img))
        )

    print("Creating val dataset")
    for img, lbl in tqdm(img_lbl_file_pth_val):
        shutil.copy(
            lbl, os.path.join(out_folder, "labels", "val", os.path.basename(lbl))
        )
        shutil.copy(
            img, os.path.join(out_folder, "images", "val", os.path.basename(img))
        )

    print("Creating test dataset")
    for img, lbl in tqdm(img_lbl_file_pth_test):
        shutil.copy(
            lbl, os.path.join(out_folder, "labels", "test", os.path.basename(lbl))
        )
        shutil.copy(
            img, os.path.join(out_folder, "images", "test", os.path.basename(img))
        )


if __name__ == "__main__":
    manualsplit(
        "out_man",
        "my_dataset_full/obj_Train_data",
        "my_dataset_full/obj_Validation_data",
        "my_dataset_full/obj_Test_data",
        "png",
        10,
        lbl_extention="txt",
    )
