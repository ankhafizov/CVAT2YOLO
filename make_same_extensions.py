import os
import shutil
from PIL import Image

def copy_files_and_convert_images(source_folder, target_folder, target_extension):
    # Create the target folder if it doesn't exist
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Normalize the target extension to lowercase
    target_extension = target_extension.lower()

    # Iterate over all files in the source folder
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        # Change the filename to include the target extension
        target_filename = os.path.splitext(filename)[0] + '.' + target_extension
        target_path = os.path.join(target_folder, target_filename)
        # Check if the file is an image
        if os.path.isfile(source_path):
            # If it's an image, convert it to the target format
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                with Image.open(source_path) as img:
                    # Determine the format based on the target extension
                    if target_extension == 'png':
                        img.save(target_path, 'PNG')
                    elif target_extension == 'jpg' or target_extension == 'jpeg':
                        img.save(target_path, 'JPEG')
                    else:
                        print(f"Unsupported target extension: {target_extension}")
                        return
            else:
                # If it's not an image, copy it as is
                shutil.copy2(source_path, os.path.join(target_folder, filename))


# Specify the path to the source folder and create a new directory next to it
source_folder = 'dataset_cvat/obj_Train_data'
target_folder = os.path.join(os.path.dirname(source_folder), 'obj_Train_data_new')

# Specify the target extension
target_extension = 'png'  # or 'jpg' or 'jpeg

# Call the function
copy_files_and_convert_images(source_folder, target_folder, target_extension)