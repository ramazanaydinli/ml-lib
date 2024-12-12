import os
import shutil

# Define the main directory path
user_path = os.path.expanduser("~")
desktop_path = os.path.join(user_path, "Desktop")

# Specify the directory containing the images and XML labels
dir_name = "single_image_trial"
dir_path = os.path.join(desktop_path, dir_name)
print(f"Main Directory Path: {dir_path}")

# Create the "Photos without Label" directory
no_label_dir_name = "Photos without Label"
no_label_dir_path = os.path.join(desktop_path, no_label_dir_name)
os.makedirs(no_label_dir_path, exist_ok=True)
print(f"'Photos without Label' Directory Path: {no_label_dir_path}")

# List all files in the main directory
all_files = os.listdir(dir_path)

# Collect all XML file names (without extension)
xml_files = {file.split('.')[0] for file in all_files if file.endswith('.xml')}

# Process photos and move those without corresponding labels
for file_name in all_files:
    if file_name.endswith(('.jpg', '.png')):
        photo_name_without_ext = os.path.splitext(file_name)[0]
        if photo_name_without_ext not in xml_files:
            # Move the photo to the "Photos without Label" directory
            source_path = os.path.join(dir_path, file_name)
            destination_path = os.path.join(no_label_dir_path, file_name)
            shutil.move(source_path, destination_path)
            print(f"Moved {source_path} to {destination_path}")
