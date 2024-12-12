import os
import cv2 as cv
import shutil
from PIL import Image

path2data = path = os.path.join("H:", "Drive'ım", "Worksight", "Data")

path2raw_images = os.path.join(path2data,"Raw Image")
path2raw_videos = os.path.join(path2data,"Raw Video")
path2processed_images = os.path.join(path2data,"Processed Image")
path2processed_videos = os.path.join(path2data,"Processed Video")
path2unlabeled = os.path.join(path2data, "Unlabeled Training Data")
path2labeled = os.path.join(path2data, "Labeled Training Data")

os.makedirs(path2processed_images, exist_ok=True)
os.makedirs(path2processed_videos, exist_ok=True)
os.makedirs(path2unlabeled, exist_ok=True)

if os.listdir(path2raw_images):
    for img_file in os.listdir(path2raw_images):
        src_path = os.path.join(path2raw_images, img_file)
        if os.path.isfile(src_path):  # Ensure it's a file
            # Move to Unlabeled Training Data
            shutil.copy(src_path, os.path.join(path2unlabeled, img_file))
            # Move to Processed Image
            shutil.move(src_path, os.path.join(path2processed_images, img_file))
    print("Images processed and moved successfully.")

if os.listdir(path2raw_videos):
    for video_file in os.listdir(path2raw_videos):
        video_path = os.path.join(path2raw_videos, video_file)
        if os.path.isfile(video_path):  # Ensure it's a file
            # Open video using OpenCV
            cap = cv.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Could not open video: {video_file}")
                continue

            # Get video FPS
            fps = int(cap.get(cv.CAP_PROP_FPS))
            frame_interval = max(1, fps // 30)  # Get one frame every half second

            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Save frame to Unlabeled Training Data at intervals
                if frame_count % frame_interval == 0:
                    frame_filename = f"{os.path.splitext(video_file)[0]}_frame_{frame_count}.jpg"
                    frame_path = os.path.join(path2unlabeled, frame_filename)
                    image = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
                    image.save(frame_path)

                frame_count += 1

            cap.release()

            # Move video to Processed Video directory
            shutil.move(video_path, os.path.join(path2processed_videos, video_file))
    print("Videos processed and frames extracted successfully.")