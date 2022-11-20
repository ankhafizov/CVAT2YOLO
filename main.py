import os

import click
import shutil

from split_auto import autosplit
from split_manual import manualsplit


TEMP_FOLDER = "TEMP"


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

    # --------------- Assertions --------------------

    assert "." not in img_format, "img_format must be without ."
    assert (
        mode == "autosplit" or mode == "manual"
    ), f"mode must be 'autosplit' or 'manual', {mode} was given"
    if mode == "autosplit":
        assert abs(split) < 1, f"float split (0<split<1) is required, {split} was given"
        assert os.path.exists(
            os.path.join(CVAT_input_folder, train_folder)
        ), f"{train_folder} does not exist in {CVAT_input_folder}"
    elif mode == "manual":
        assert (
            os.path.exists(train_folder)
            or os.path.exists(val_folder)
            or os.path.exists(test_folder)
        ), f"At least one of {train_folder}, {val_folder} and {test_folder} must exist in {CVAT_input_folder}"
        if split is not None:
            print("WARNING: skipping split value n manual mode")

    # --------------------- main --------------------
    CVAT_backup_folder = f"{CVAT_input_folder}_backup"
    shutil.copytree(CVAT_input_folder, CVAT_backup_folder)

    if mode == "autosplit":
        autosplit(
            output_folder,
            os.path.join(CVAT_input_folder, train_folder),
            os.path.join(CVAT_input_folder, val_folder),
            os.path.join(CVAT_input_folder, test_folder),
            img_format,
            split,
            percentage_empty,
            lbl_extention="txt",
        )
    elif mode == "manual":
        manualsplit(
            output_folder,
            os.path.join(CVAT_input_folder, train_folder),
            os.path.join(CVAT_input_folder, val_folder),
            os.path.join(CVAT_input_folder, test_folder),
            img_format,
            percentage_empty,
            lbl_extention="txt",
        )

    shutil.rmtree(CVAT_input_folder)
    os.rename(CVAT_backup_folder, CVAT_input_folder)
    # -----------------------------------------------


if __name__ == "__main__":
    main()
