import os


user_path = os.path.expanduser("~")
desktop_path = os.path.join(user_path, "Desktop")


# Open a directory in desktop and name it whatever you want and change the name below accordingly
# For example the code below assumes your directory name as "statics_images"

dir_name = "static training images"
dir_path = os.path.join(desktop_path, dir_name, "images")


all_files = os.listdir(dir_path)
png_files = {file.split('.')[0] for file in all_files if file.endswith('.png')}
xml_files = {file.split('.')[0] for file in all_files if file.endswith('.xml')}

xml_without_png = xml_files - png_files

for file_name in xml_without_png:
        xml_file_path = os.path.join(dir_path, file_name + '.xml')
        if os.path.exists(xml_file_path):
            os.remove(xml_file_path)
            print(f"Removed {xml_file_path}")

