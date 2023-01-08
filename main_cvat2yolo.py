import os

import click
import shutil
import yaml

from split_auto import autosplit
from split_manual import manualsplit
from lib_utils_cvat2yolo import (
    create_YOLOv5_folder_tree,
    remove_unwanted_classes,
    transform_cls_labels,
)


def get_datset_classes(names_file, classes_to_keep):
    with open(names_file) as f:
        dataset_names = f.read().splitlines()

    if classes_to_keep == "keep-all":
        return dataset_names
    else:
        print(classes_to_keep)
        classes_to_keep = classes_to_keep.split("|")
        print(classes_to_keep)
        names = [n for n in dataset_names if n in classes_to_keep]
        if len(names) == 0:
            raise ValueError(
                f"--classes arg is not valid, dataset classes: {dataset_names}"
            )
        print(f"KEEPING CLASSES: {names}")
        return names


def form_yaml_file(output_folder, classes):
    number_of_classes = len(classes)
    path = os.path.join("data", output_folder)
    train = os.path.join("images", "train")
    val = os.path.join("images", "val")
    test = os.path.join("images", "test")

    with open(f"{output_folder}.yaml", "w") as stream:
        yaml.dump(
            {
                "names": classes,
                "nc": number_of_classes,
                "path": path,
                "train": train,
                "val": val,
                "test": test,
            },
            stream,
            default_flow_style=False,
        )


@click.command()
@click.option(
    "--cvat",
    help="Path to the root folder of imported from CVAT YOLO 1.1 dataset",
    required=True,
    type=str,
)
@click.option(
    "--mode",
    help="'autosplit' or 'manual' (as it was exported from CVAT)",
    required=True,
    type=str,
)
@click.option(
    "--output_folder",
    help="Path to converted dataset folder, e.g. in format {root}/{dataset name}",
    required=True,
    type=str,
)
@click.option(
    "--split",
    help="A percentage of a split, e.g. 0.9 means split 0.9 for train and 0.1 for test",
    type=float,
)
@click.option(
    "--label_tfrms",
    help="Label union with another existed in dataset (example: 'head->hood,helmet->hat')",
    default=None,
    type=str,
)
@click.option(
    "--train_folder",
    default="obj_Train_data",
    help="Folder with Train subset inside cvat path (default obj_Train_data)",
    type=str,
)
@click.option(
    "--val_folder",
    default="obj_Validation_data",
    help="Folder with Val subset inside cvat path (default obj_Validation_data)",
    type=str,
)
@click.option(
    "--test_folder",
    default="obj_Test_data",
    help="Folder with Test subset inside cvat path (default obj_Test_data)",
    type=str,
)
@click.option("--img_format", default="png", help="Format of images", type=str)
@click.option(
    "--percentage_empty",
    default=10,
    help="Percentage of images without any labels in relation to full dataset size",
    type=float,
)
@click.option(
    "--classes", default="keep-all", help="Classes which labels to keep", type=str
)
def main(**kwargs):

    # ------------------ ARG parse ------------------
    CVAT_input_folder = kwargs["cvat"]
    mode = kwargs["mode"]
    output_folder = kwargs["output_folder"]
    split = kwargs["split"]
    train_folder = kwargs["train_folder"]
    val_folder = kwargs["val_folder"]
    test_folder = kwargs["test_folder"]
    percentage_empty = int(kwargs["percentage_empty"])
    img_format = kwargs["img_format"]
    label_tfrms = kwargs["label_tfrms"]

    CVAT_work_folder = f"{CVAT_input_folder}_copy"
    shutil.copytree(CVAT_input_folder, CVAT_work_folder)
    names_file = "obj.names"
    names_file_pth = os.path.join(CVAT_work_folder, names_file)
    train_folder = os.path.join(CVAT_work_folder, train_folder)
    val_folder = os.path.join(CVAT_work_folder, val_folder)
    test_folder = os.path.join(CVAT_work_folder, test_folder)
    classes_to_keep = kwargs["classes"]

    # --------------- Assertions --------------------

    assert "." not in img_format, "img_format must be without ."
    assert (
        mode == "autosplit" or mode == "manual"
    ), f"mode must be 'autosplit' or 'manual', {mode} was given"
    if mode == "autosplit":
        assert abs(split) < 1, f"float split (0<split<1) is required, {split} was given"
        assert os.path.exists(
            os.path.join(CVAT_work_folder, train_folder)
        ), f"{train_folder} does not exist in {CVAT_work_folder}"
    elif mode == "manual":
        assert (
            os.path.exists(train_folder)
            or os.path.exists(val_folder)
            or os.path.exists(test_folder)
        ), f"At least one of {train_folder}, {val_folder} and {test_folder} must exist"
        if split is not None:
            print("WARNING: skipping split value n manual mode")

    # --------------------- main --------------------
    create_YOLOv5_folder_tree(output_folder)

    if label_tfrms is not None:
        transform_cls_labels(CVAT_work_folder, names_file_pth, label_tfrms)

    classes_to_keep = get_datset_classes(names_file_pth, classes_to_keep)
    remove_unwanted_classes(CVAT_work_folder, names_file_pth, classes_to_keep)

    form_yaml_file(output_folder, classes_to_keep)

    if mode == "autosplit":
        autosplit(
            output_folder,
            train_folder,
            val_folder,
            test_folder,
            img_format,
            split,
            percentage_empty,
            lbl_extention="txt",
        )
    elif mode == "manual":
        manualsplit(
            output_folder,
            train_folder,
            val_folder,
            test_folder,
            img_format,
            percentage_empty,
            lbl_extention="txt",
        )

    shutil.rmtree(CVAT_work_folder)
    # -----------------------------------------------


if __name__ == "__main__":
    main()
