import os
from random import shuffle

from glob import glob
import shutil

from tqdm import tqdm

from lib_utils_cvat2yolo import is_txt_file_empty


def get_file_paths_lists_for_training(
    train_folder_pth, val_folder_pth, img_extention, lbl_extention
):
    img_file_pths = []
    lbl_file_pths = []

    if os.path.exists(train_folder_pth):
        img_file_pths.extend(glob(f"{train_folder_pth}/*.{img_extention}"))

    if os.path.exists(val_folder_pth):
        img_file_pths.extend(glob(f"{val_folder_pth}/*.{img_extention}"))

    shuffle(img_file_pths)
    lbl_file_pths.extend(
        [p.replace(f".{img_extention}", f".{lbl_extention}") for p in img_file_pths]
    )

    return list(zip(img_file_pths, lbl_file_pths))


def get_file_paths_lists_for_test(test_folder_pth, img_extention, lbl_extention):
    img_file_pths = []
    lbl_file_pths = []

    if os.path.exists(test_folder_pth):
        img_file_pths.extend(glob(f"{test_folder_pth}/*.{img_extention}"))

    lbl_file_pths.extend(
        [p.replace(f".{img_extention}", f".{lbl_extention}") for p in img_file_pths]
    )

    return list(zip(img_file_pths, lbl_file_pths))


def split_train_val(lst, split_ratio):
    N = int(len(lst) * split_ratio)
    return lst[:N], lst[N:]


def autosplit(
    out_folder,
    train_folder_pth,
    val_folder_pth,
    test_folder_pth,
    img_extention,
    split_ratio,
    percentage_empty,
    lbl_extention="txt",
):

    img_lbl_file_pth_training = get_file_paths_lists_for_training(
        train_folder_pth, val_folder_pth, img_extention, lbl_extention
    )
    img_lbl_file_pth_test = get_file_paths_lists_for_test(
        test_folder_pth, img_extention, lbl_extention
    )

    img_lbl_file_pth_train, img_lbl_file_pth_val = split_train_val(
        img_lbl_file_pth_training, split_ratio
    )

    print(f"Creating train dataset | {out_folder}")
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

    print(f"Creating val dataset | {out_folder}")
    for img, lbl in tqdm(img_lbl_file_pth_val):
        shutil.copy(
            lbl, os.path.join(out_folder, "labels", "val", os.path.basename(lbl))
        )
        shutil.copy(
            img, os.path.join(out_folder, "images", "val", os.path.basename(img))
        )

    print(f"Creating test dataset | {out_folder}")
    for img, lbl in tqdm(img_lbl_file_pth_test):
        shutil.copy(
            lbl, os.path.join(out_folder, "labels", "test", os.path.basename(lbl))
        )
        shutil.copy(
            img, os.path.join(out_folder, "images", "test", os.path.basename(img))
        )


if __name__ == "__main__":
    autosplit(
        "out",
        "my_dataset_full/obj_Train_data",
        "my_dataset_full/obj_Validation_data",
        "my_dataset_full/obj_Test_data",
        "png",
        0.9,
        10,
        lbl_extention="txt",
    )
