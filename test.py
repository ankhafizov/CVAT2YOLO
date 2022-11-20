from glob import glob
import cv2
import random
import yaml


font = cv2.FONT_HERSHEY_COMPLEX
color = (0, 255, 255)


def _downscale_frame(img, frame_scale):
    width = int(img.shape[1] * frame_scale)
    height = int(img.shape[0] * frame_scale)
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    return img


def draw_label(img, label, classes, img_pth):
    label_name, xc, yc, xw, yw = label.split(" ")
    label_name = classes[int(label_name)]

    xc, yc, xw, yw = float(xc), float(yc), float(xw), float(yw)
    y_shape, x_shape = img.shape[0], img.shape[1]
    x1 = int((xc - xw / 2) * x_shape)
    x2 = int((xc + xw / 2) * x_shape)
    y1 = int((yc - yw / 2) * y_shape)
    y2 = int((yc + yw / 2) * y_shape)

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.putText(img, label_name, (x1, y1), font, 3, color, 2)
    cv2.putText(img, img_pth, (50, 50), font, 4, color, 2)
    return img


def draw_labels(
    yolov5_dataset_pth, subset, frame_scale, img_extention="png", lbl_extention="txt"
):

    img_pths = glob(f"{yolov5_dataset_pth}/images/{subset}/*.{img_extention}")
    with open(f"{yolov5_dataset_pth}.yaml", "r") as stream:
        cfg = yaml.safe_load(stream)
        classes = cfg["names"]

    while True:
        img_pth = random.choice(img_pths)
        img = cv2.imread(img_pth)

        lbl_pth = img_pth.replace("images", "labels").replace(
            f".{img_extention}", f".{lbl_extention}"
        )

        with open(lbl_pth, "r") as f:
            lable_lines = f.readlines()
            for label in lable_lines:
                img = draw_label(img, label, classes, img_pth)

        img = _downscale_frame(img, frame_scale)
        cv2.imshow("Frame", img)
        cv2.waitKey(0)


if __name__ == "__main__":
    draw_labels("out", "val", frame_scale=0.5)
