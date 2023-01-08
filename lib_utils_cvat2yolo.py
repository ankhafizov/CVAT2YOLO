from pathlib import Path
import shutil
from glob import glob
from copy import deepcopy

from tqdm import tqdm


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


def _get_cls_indx_from_line(line):
    return int(line.split(" ")[0])


def _replace_indx_in_line(line, new_indx):
    line = line.split(" ")
    line[0] = str(new_indx)
    return " ".join(line)


def _correct_cls_in_txt_file(txt_file_pth, indxs_to_keep, old_new_indexes_hash_map):
    new_lines = []
    with open(txt_file_pth) as f:
        lines = f.readlines()
        for line in lines:
            current_indx = _get_cls_indx_from_line(line)
            if current_indx in indxs_to_keep:
                new_indx = old_new_indexes_hash_map[current_indx]
                new_line = _replace_indx_in_line(line, new_indx)
                new_lines.append(new_line)

    with open(txt_file_pth, "w") as f:
        for line in new_lines:
            f.write(line)


def update_names_file(names_file_pth, new_classes):
    with open(names_file_pth, "w") as f:
        for line in new_classes:
            f.write(line)


def remove_unwanted_classes(CVAT_input_folder, names_file_pth, classes_to_keep):
    with open(names_file_pth) as f:
        classes_original = f.read().splitlines()

    indxs_to_keep = [classes_original.index(cls) for cls in classes_to_keep]
    old_new_indexes_hash_map = {
        indx_old: indx_new for indx_new, indx_old in enumerate(indxs_to_keep)
    }

    for txt_file_pth in tqdm(glob(f"{CVAT_input_folder}/*/*.txt")):
        _correct_cls_in_txt_file(txt_file_pth, indxs_to_keep, old_new_indexes_hash_map)

    update_names_file(names_file_pth, classes_to_keep)


def transform_cls_labels(CVAT_input_folder, names_file_pth, label_tfrms):
    with open(names_file_pth) as f:
        classes_original = f.read().splitlines()

    classes_new = deepcopy(classes_original)

    label_tfrms = label_tfrms.split(",")
    for label_tfrm in label_tfrms:
        old_label, new_label = label_tfrm.split("->")
        assert (
            old_label in classes_original
        ), f"label_tfrm old_label {old_label} not in dataset classes {classes_original}"
        assert (
            new_label in classes_original
        ), f"label_tfrm new_label {new_label} not in dataset classes {classes_original}"

        classes_new = list(map(lambda x: x.replace(old_label, new_label), classes_new))

    if classes_original == classes_new:
        return

    old_new_indexes_hash_map = {
        i: classes_original.index(cls) for i, cls in enumerate(classes_new)
    }

    print(f"label_tfrms : {label_tfrms}")
    for txt_file_pth in tqdm(glob(f"{CVAT_input_folder}/*/*.txt")):
        _correct_cls_in_txt_file(
            txt_file_pth, range(len(classes_original)), old_new_indexes_hash_map
        )


if __name__ == "__main__":
    remove_unwanted_classes("my_dataset_full", "my_dataset_full/obj.names", ["helmet"])
