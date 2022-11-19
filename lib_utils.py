from pathlib import Path
import shutil


def create_YOLOv5_folder_tree(out_folder):
    try:
        shutil.rmtree(out_folder)
    except FileNotFoundError:
        pass

    Path(out_folder, "images", "train").mkdir(parents=True, exist_ok=False)
    Path(out_folder, "images", "val").mkdir(parents=True, exist_ok=False)
    Path(out_folder, "images", "test").mkdir(parents=True, exist_ok=False)

    Path(out_folder, "labels", "train").mkdir(parents=True, exist_ok=False)
    Path(out_folder, "labels", "val").mkdir(parents=True, exist_ok=False)
    Path(out_folder, "labels", "test").mkdir(parents=True, exist_ok=False)


def is_txt_file_empty(file_pth):
    with open(file_pth) as f:
        return f.read() == ""
