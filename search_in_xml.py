import os
import xml.etree.ElementTree as ET

def search_pointer_in_xml(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    # Search for the exact word "fix_support" in the text content
    for elem in root.iter():
        if elem.text == "pin_support_v":
            return True

    return False

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                if search_pointer_in_xml(file_path):
                    print("File with pointer found:", file_path)

user_path = os.path.expanduser("~")
desktop_path = os.path.join(user_path, "Desktop")

dir_name = "full etiketli 1200 str 44 etiket"
dir_path = os.path.join(desktop_path, dir_name)

process_directory(dir_path)
