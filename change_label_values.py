import os
import re

def correct_spacing_in_xml(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Correcting spacing_h to spacing
    corrected_content = re.sub(r'equ_\w+', 'formulized_distributed_load', content)

    with open(file_path, 'w') as file:
        file.write(corrected_content)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                correct_spacing_in_xml(file_path)

user_path = os.path.expanduser("~")
desktop_path = os.path.join(user_path, "Desktop")

dir_name = "str v4"
dir_path = os.path.join(desktop_path, dir_name)

process_directory(dir_path)
