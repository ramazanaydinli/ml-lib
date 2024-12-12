import os
import cv2
import xml.etree.ElementTree as ET

def parse_annotations(xml_file):
    """
    Parse the Pascal VOC XML annotation file and extract bounding boxes and labels.

    Args:
        xml_file (str): Path to the XML annotation file.

    Returns:
        dict: Dictionary containing image size, bounding boxes, and labels.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Get image size
    width = int(root.find("size/width").text)
    height = int(root.find("size/height").text)

    annotations = []
    for obj in root.findall("object"):
        label = obj.find("name").text
        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)
        annotations.append({"label": label, "bbox": (xmin, ymin, xmax, ymax)})

    return {"width": width, "height": height, "annotations": annotations}

def draw_annotations(image, annotations):
    """
    Draw bounding boxes and labels on an image with specific colors for each class.

    Args:
        image (numpy.ndarray): The image to annotate.
        annotations (list): List of bounding box dictionaries.

    Returns:
        numpy.ndarray: Annotated image.
    """
    # Define colors for each class
    class_colors = {
        "person": (128, 0, 128),  # Purple
        "hook_safe": (255, 0, 0),  # Red
        "hook_unsafe": (0, 0, 255),  # Blue
    }

    for ann in annotations:
        label = ann["label"]
        xmin, ymin, xmax, ymax = ann["bbox"]

        # Draw the bounding box (always green)
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 1)

        # Get the color for the label (default to white if not in class_colors)
        font_color = class_colors.get(label, (255, 255, 255))

        # Put the label text
        cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, font_color, 2)

    return image


def natural_sort(file_list):
    """
    Sort filenames containing numbers in natural order (e.g., image1, image2, image10).

    Args:
        file_list (list): List of filenames.

    Returns:
        list: Naturally sorted list of filenames.
    """
    return sorted(file_list, key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

def create_video_from_annotations(data_dir, output_video, fps=30):
    """
    Create a video with bounding boxes drawn from annotations.

    Args:
        data_dir (str): Directory containing image and XML files.
        output_video (str): Path to the output video file.
        fps (int): Frames per second for the video.

    Returns:
        None
    """
    # Get all image files
    files = os.listdir(data_dir)
    image_files = [f for f in files if f.endswith((".jpg", ".png"))]
    image_files = natural_sort(image_files)  # Sort numerically

    if not image_files:
        print("No images found in the directory.")
        return

    # Get image size from the first image
    sample_image_path = os.path.join(data_dir, image_files[0])
    sample_image = cv2.imread(sample_image_path)
    if sample_image is None:
        print("Error reading the sample image.")
        return

    height, width, _ = sample_image.shape

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    if not video_writer.isOpened():
        print(f"Failed to open video writer with path: {output_video}")
        return

    # Process each image
    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        xml_file = os.path.join(data_dir, base_name + ".xml")

        # Read image
        image_path = os.path.join(data_dir, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error reading image: {image_path}")
            continue

        # Parse annotations
        if os.path.exists(xml_file):
            annotations = parse_annotations(xml_file)
            image = draw_annotations(image, annotations["annotations"])

        # Write frame to video
        video_writer.write(image)

    # Release video writer
    video_writer.release()
    print(f"Video saved to {output_video}")

if __name__ == "__main__":
    # Path to your data directory
    user_path = os.path.expanduser("~")
    desktop_path = os.path.join(user_path, "Desktop")

    # Open a directory in desktop and name it whatever you want and change the name below accordingly
    # For example the code below assumes your directory name as "statics_images"

    dir_name = "single_image_trial"
    dir_path = os.path.join(desktop_path, dir_name)
    DATA_DIR = dir_path  # Directory containing images and XML files
    OUTPUT_VIDEO = "output_video.mp4"  # Output video file

    # Create video
    create_video_from_annotations(DATA_DIR, OUTPUT_VIDEO, fps=30)
