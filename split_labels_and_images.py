from glob import glob
from pathlib import Path
import shutil
import os
from tqdm import tqdm


def _is_txt_file_empty(file_pth):
    with open(file_pth) as f:
        return f.read() == ""


def split_lbl_img(in_folder, out_folder, img_format, percentage_of_empty_files):
    Path(out_folder, "labels").mkdir(parents=True, exist_ok=True)
    Path(out_folder, "images").mkdir(parents=True, exist_ok=True)

    lbl_file_pths = glob(f"{in_folder}/obj_train_data/*.txt")
    img_file_pths = glob(f"{in_folder}/obj_train_data/*.{img_format}")

    N_files = len(lbl_file_pths)
    acceptable_N_of_empty_files = int(N_files * percentage_of_empty_files / 100)

    lbl_file_pths.sort()
    img_file_pths.sort()

    count_of_empty_files = 0
    logged_empty_count = False

    for lbl_file, img_file in tqdm(
        zip(lbl_file_pths, img_file_pths), total=len(img_file_pths)
    ):
        if _is_txt_file_empty(lbl_file):
            count_of_empty_files += 1
            if count_of_empty_files < acceptable_N_of_empty_files:
                pass
            else:
                if not logged_empty_count:
                    print(f"Empty count: {count_of_empty_files} / {N_files}")
                    logged_empty_count = True
                continue

        basename_lbl = os.path.basename(lbl_file)
        basename_img = os.path.basename(img_file)
        shutil.copyfile(lbl_file, os.path.join(out_folder, "labels", basename_lbl))
        shutil.copyfile(img_file, os.path.join(out_folder, "images", basename_img))

    shutil.copyfile(f"{in_folder}/obj.names", f"{out_folder}/obj.names")


if __name__ == "__main__":
    split_lbl_img(
        "task_сизы 10.06.2022-2022_10_07_14_51_13-yolo 1.1", "dataset2", "png", 10
    )
