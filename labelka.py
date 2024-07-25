# import os
# import glob
# import cv2

# bounding_boxes = []
# current_box = []
# keypoints = []
# drawing_box = False
# drawing_keypoints = False
# start_point = None
# output_folder = 'data/labels/train'
# counter = 17
# show_save_message = False

# def read_images(folder_path):
#     image_formats = ('*.jpg', '*.jpeg', '*.png')
#     image_files = []
#     for image_format in image_formats:
#         image_files.extend(glob.glob(os.path.join(folder_path, image_format)))
#     return image_files

# def mouse_callback(event, x, y, flags, param):
#     global current_box, drawing_box, drawing_keypoints, start_point, keypoints, counter, show_save_message
    
#     if event == cv2.EVENT_MBUTTONDOWN:
#         if not drawing_box:
#             start_point = (x, y)
#             drawing_box = True
#         else:
#             current_box = [start_point, (x, y)]
#             drawing_box = False
#             drawing_keypoints = True
#             bounding_boxes.append(current_box)
#             update_counter()

#     elif event == cv2.EVENT_MOUSEMOVE and drawing_box:
#         current_box = [start_point, (x, y)]

#     elif event == cv2.EVENT_LBUTTONDOWN and drawing_keypoints:
#         keypoints.append((x, y))
#         update_counter()

# def update_counter():
#     global counter, show_save_message
#     counter -= 1
#     if counter < 0:
#         counter = 17
#         show_save_message = True

# def revert_counter():
#     global counter
#     counter += 1
#     if counter > 17:
#         counter = 0

# def save_bounding_boxes(image_file, bounding_boxes, keypoints, img_width, img_height):
#     txt_file_name = os.path.splitext(os.path.basename(image_file))[0] + '.txt'
#     txt_file_path = os.path.join(output_folder, txt_file_name)

#     with open(txt_file_path, 'a') as f:
#         for box in bounding_boxes:
#             x1, y1 = box[0]
#             x2, y2 = box[1]
#             x_center = (x1 + x2) / 2 / img_width
#             y_center = (y1 + y2) / 2 / img_height
#             width = abs(x2 - x1) / img_width
#             height = abs(y2 - y1) / img_height
#             f.write(f"0 {x_center} {y_center} {width} {height}")
#             for i in range(len(keypoints)):
#                 x_kp = keypoints[i][0] / img_width
#                 y_kp = keypoints[i][1] / img_height
#                 f.write(f" {x_kp} {y_kp}")
#             f.write("\n")
    
#     print(f"Bounding boxes and keypoints saved to {txt_file_path}")

# def display_images(image_files):
#     global current_box, drawing_box, drawing_keypoints, start_point, image_file, keypoints, counter, show_save_message

#     index = 0
#     total_images = len(image_files)
    
#     if total_images == 0:
#         print("No images found in the specified folder.")
#         return

#     cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)
#     cv2.setMouseCallback('Image', mouse_callback)

#     instructions = [
#         "Right Ankle", "Left Ankle", "Right Knee", "Left Knee", 
#         "Right Hip", "Left Hip", "Right Wrist", "Left Wrist", 
#         "Right Elbow", "Left Elbow", "Right Shoulder", "Left Shoulder", 
#         "Right Ear", "Left Ear", "Right Eye", "Left Eye", 
#         "Nose", "Bounding box"
#     ]

#     while True:
#         image_file = image_files[index]
#         image = cv2.imread(image_file)
#         image_copy = image.copy()
#         img_height, img_width = image.shape[:2]

#         if image is not None:
#             for box in bounding_boxes:
#                 cv2.rectangle(image_copy, box[0], box[1], (255, 0, 0), 2)
#             if len(current_box) == 2:
#                 cv2.rectangle(image_copy, current_box[0], current_box[1], (255, 0, 0), 2)
#             for kp in keypoints:
#                 if isinstance(kp, tuple):
#                     cv2.circle(image_copy, (int(kp[0]), int(kp[1])), 3, (0, 255, 0), -1)
            
#             current_instruction = f"{counter}: {instructions[counter]}"
#             cv2.putText(image_copy, f"Number of keypoints remaining: {counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
#             cv2.putText(image_copy, f"Image: {os.path.basename(image_file)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
#             cv2.putText(image_copy, current_instruction, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            
#             if show_save_message:
#                 text = "Press the 's' key to save"
#                 text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
#                 text_x = (img_width - text_size[0]) // 2
#                 cv2.putText(image_copy, text, (text_x, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

#             cv2.imshow('Image', image_copy)
#             print(f"Displaying {image_file}. Press 'a' for previous, 'd' for next, 's' to save, 'q' to quit, 'z' to skip keypoint, 'r' to delete last action.")

#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('d'):
#                 index = (index + 1) % total_images
#                 bounding_boxes.clear()
#                 keypoints.clear()
#                 current_box = []
#                 drawing_box = False
#                 drawing_keypoints = False
#                 start_point = None
#                 counter = 17
#                 show_save_message = False
#             elif key == ord('a'):
#                 index = (index - 1 + total_images) % total_images
#                 bounding_boxes.clear()
#                 keypoints.clear()
#                 current_box = []
#                 drawing_box = False
#                 drawing_keypoints = False
#                 start_point = None
#                 counter = 17
#                 show_save_message = False
#             elif key == ord('s'):
#                 save_bounding_boxes(image_file, bounding_boxes, keypoints, img_width, img_height)
#                 bounding_boxes.clear()
#                 keypoints.clear()
#                 current_box = []
#                 drawing_box = False
#                 drawing_keypoints = False
#                 start_point = None
#                 counter = 17
#                 show_save_message = False
#             elif key == ord('q'):
#                 break
#             elif key == ord('z') and drawing_keypoints:
#                 keypoints.append((0, 0))
#                 update_counter()
#             elif key == ord('r'):
#                 if keypoints:
#                     keypoints.pop()
#                     revert_counter()
#                 elif bounding_boxes:
#                     bounding_boxes.pop()
#                     current_box = []
#                     drawing_keypoints = False
#                     drawing_box = False
#                     start_point = None
#                     revert_counter()
#         else:
#             print(f"Failed to load image: {image_file}")
    
#     cv2.destroyAllWindows()

# def main():
#     folder_path = 'data/images/train'
    
#     image_files = read_images(folder_path)
#     display_images(image_files)

# if __name__ == "__main__":
#     main()


import os
import glob
import cv2

bounding_boxes = []
current_box = []
keypoints = []
drawing_box = False
drawing_keypoints = False
start_point = None
output_folder = 'data/labels/train'
counter = 17
show_save_message = False

colors = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 0, 255), (0, 255, 255),
    (128, 0, 0), (0, 128, 0), (0, 0, 128),
    (128, 128, 0)
]

def read_images(folder_path):
    image_formats = ('*.jpg', '*.jpeg', '*.png')
    image_files = []
    for image_format in image_formats:
        image_files.extend(glob.glob(os.path.join(folder_path, image_format)))
    return image_files

def read_labels(label_file_path, img_width, img_height):
    bounding_boxes = []
    keypoints = []

    if os.path.exists(label_file_path):
        with open(label_file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                x1 = int((x_center - width / 2) * img_width)
                y1 = int((y_center - height / 2) * img_height)
                x2 = int((x_center + width / 2) * img_width)
                y2 = int((y_center + height / 2) * img_height)
                bounding_boxes.append([(x1, y1), (x2, y2)])
                keypoints.append([(float(parts[i]) * img_width, float(parts[i+1]) * img_height) for i in range(5, len(parts), 2)])
    return bounding_boxes, keypoints

def mouse_callback(event, x, y, flags, param):
    global current_box, drawing_box, drawing_keypoints, start_point, keypoints, counter, show_save_message
    
    if event == cv2.EVENT_MBUTTONDOWN:
        if not drawing_box:
            start_point = (x, y)
            drawing_box = True
        else:
            current_box = [start_point, (x, y)]
            drawing_box = False
            drawing_keypoints = True
            bounding_boxes.append(current_box)
            keypoints.append([])
            update_counter()

    elif event == cv2.EVENT_MOUSEMOVE and drawing_box:
        current_box = [start_point, (x, y)]

    elif event == cv2.EVENT_LBUTTONDOWN and drawing_keypoints:
        keypoints[-1].append((x, y))
        update_counter()

def update_counter():
    global counter, show_save_message
    counter -= 1
    if counter < 0:
        counter = 17
        show_save_message = True

def revert_counter():
    global counter
    counter += 1
    if counter > 17:
        counter = 0

def save_bounding_boxes(image_file, bounding_boxes, keypoints, img_width, img_height):
    txt_file_name = os.path.splitext(os.path.basename(image_file))[0] + '.txt'
    txt_file_path = os.path.join(output_folder, txt_file_name)

    with open(txt_file_path, 'w') as f:
        for box, kps in zip(bounding_boxes, keypoints):
            x1, y1 = box[0]
            x2, y2 = box[1]
            x_center = (x1 + x2) / 2 / img_width
            y_center = (y1 + y2) / 2 / img_height
            width = abs(x2 - x1) / img_width
            height = abs(y2 - y1) / img_height
            f.write(f"0 {x_center} {y_center} {width} {height}")
            for kp in kps:
                x_kp = kp[0] / img_width
                y_kp = kp[1] / img_height
                f.write(f" {x_kp} {y_kp}")
            f.write("\n")
    
    print(f"Bounding boxes and keypoints saved to {txt_file_path}")

def display_images(image_files):
    global current_box, drawing_box, drawing_keypoints, start_point, image_file, keypoints, counter, show_save_message

    index = 0
    total_images = len(image_files)
    
    if total_images == 0:
        print("No images found in the specified folder.")
        return

    cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback('Image', mouse_callback)

    instructions = [
        "Right Ankle", "Left Ankle", "Right Knee", "Left Knee", 
        "Right Hip", "Left Hip", "Right Wrist", "Left Wrist", 
        "Right Elbow", "Left Elbow", "Right Shoulder", "Left Shoulder", 
        "Right Ear", "Left Ear", "Right Eye", "Left Eye", 
        "Nose", "Bounding box"
    ]

    while True:
        image_file = image_files[index]
        image = cv2.imread(image_file)
        image_copy = image.copy()
        img_height, img_width = image.shape[:2]

        label_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(image_file))[0] + '.txt')
        saved_bounding_boxes, saved_keypoints = read_labels(label_file_path, img_width, img_height)

        if image is not None:
            for i, box in enumerate(saved_bounding_boxes):
                color = colors[i % len(colors)]
                cv2.rectangle(image_copy, box[0], box[1], color, 2)
                for kp in saved_keypoints[i]:
                    if isinstance(kp, tuple):
                        cv2.circle(image_copy, (int(kp[0]), int(kp[1])), 3, color, -1)

            for i, box in enumerate(bounding_boxes):
                cv2.rectangle(image_copy, box[0], box[1], colors[i % len(colors)], 2)
                for kp in keypoints[i]:
                    if isinstance(kp, tuple):
                        cv2.circle(image_copy, (int(kp[0]), int(kp[1])), 3, colors[i % len(colors)], -1)
            
            if len(current_box) == 2:
                cv2.rectangle(image_copy, current_box[0], current_box[1], colors[len(bounding_boxes) % len(colors)], 2)
            for kp in keypoints[-1] if keypoints else []:
                if isinstance(kp, tuple):
                    cv2.circle(image_copy, (int(kp[0]), int(kp[1])), 3, colors[len(bounding_boxes) % len(colors)], -1)
            
            current_instruction = f"{counter}: {instructions[counter]}"
            cv2.putText(image_copy, f"Number of keypoints remaining: {counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image_copy, f"Image: {os.path.basename(image_file)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image_copy, current_instruction, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            
            if show_save_message:
                text = "Press the 's' key to save"
                text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                text_x = (img_width - text_size[0]) // 2
                cv2.putText(image_copy, text, (text_x, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Image', image_copy)
            print(f"Displaying {image_file}. Press 'a' for previous, 'd' for next, 's' to save, 'q' to quit, 'z' to skip keypoint, 'r' to delete last action.")

            key = cv2.waitKey(1) & 0xFF
            if key == ord('d'):
                index = (index + 1) % total_images
                bounding_boxes.clear()
                keypoints.clear()
                current_box = []
                drawing_box = False
                drawing_keypoints = False
                start_point = None
                counter = 17
                show_save_message = False
            elif key == ord('a'):
                index = (index - 1 + total_images) % total_images
                bounding_boxes.clear()
                keypoints.clear()
                current_box = []
                drawing_box = False
                drawing_keypoints = False
                start_point = None
                counter = 17
                show_save_message = False
            elif key == ord('s'):
                save_bounding_boxes(image_file, bounding_boxes, keypoints, img_width, img_height)
                bounding_boxes.clear()
                keypoints.clear()
                current_box = []
                drawing_box = False
                drawing_keypoints = False
                start_point = None
                counter = 17
                show_save_message = False
            elif key == ord('q'):
                break
            elif key == ord('z') and drawing_keypoints:
                keypoints[-1].append((0, 0))
                update_counter()
            elif key == ord('r'):
                if keypoints and keypoints[-1]:
                    keypoints[-1].pop()
                    update_counter()
                elif bounding_boxes:
                    bounding_boxes.pop()
                    keypoints.pop()
                    current_box = []
                    drawing_keypoints = False
                    drawing_box = False
                    start_point = None
                    revert_counter()
        else:
            print(f"Failed to load image: {image_file}")
    
    cv2.destroyAllWindows()

def main():
    folder_path = 'data/images/train'
    
    image_files = read_images(folder_path)
    display_images(image_files)

if __name__ == "__main__":
    main()
