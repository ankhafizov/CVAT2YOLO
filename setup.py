from setuptools import find_packages
from distutils.core import setup

setup(
    name="CVAT2YOLO",
    version="1.0",
    packages=find_packages(),
    long_description="Converts CVAT YOLO 1.1 to COCO format",
    include_package_data=True,
    entry_points={
        "console_scripts": ["cvat2yolo=main_cvat2yolo:main"],
    },
    install_requires=[
        "PyYAML==6.0",
    ],
)
