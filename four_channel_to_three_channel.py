import cv2
import os


user_path = os.path.expanduser("~")
desktop_path = os.path.join(user_path, "Desktop")
dir_name = "geo_trial1"
dir_path = os.path.join(desktop_path, dir_name)


image_paths = []
for image_name in os.listdir(dir_path):
    image_paths.append(os.path.join(dir_path, image_name))

for img in image_paths:
    print(img)
    # Load the 4-channel image
    image_4_channel = cv2.imread(img, cv2.IMREAD_UNCHANGED)

    # Convert to 3-channel image
    if image_4_channel.shape[2] == 4:  # Check if it's a 4-channel image
        image_3_channel = cv2.cvtColor(image_4_channel, cv2.COLOR_BGRA2BGR)  # Convert from BGRA to BGR
        # Or, you can simply drop the alpha channel
        # image_3_channel = image_4_channel[:, :, :3]

    else:
        # It's already a 3-channel image
        image_3_channel = image_4_channel

    # Save the 3-channel image
    cv2.imwrite(img, image_3_channel)
