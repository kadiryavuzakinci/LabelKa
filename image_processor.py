import os
import glob
import cv2
from label_manager import LabelManager
import threading

class ImageProcessor:
    def __init__(self, folder_path, output_folder, ui_handler):
        self.folder_path = folder_path
        self.output_folder = output_folder
        self.ui_handler = ui_handler
        self.label_manager = LabelManager(output_folder)
        self.bounding_boxes = []
        self.keypoints = []
        self.current_box = []
        self.drawing_box = False
        self.drawing_keypoints = False
        self.start_point = None
        self.counter = 17
        self.show_save_message = False
        self.save_message_displayed = False
        self.bounding_box_ids = []

        self.colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (128, 0, 0), (0, 128, 0), (0, 0, 128),
            (128, 128, 0)
        ]

    def read_images(self):
        image_formats = ('*.jpg', '*.jpeg', '*.png')
        image_files = []
        for image_format in image_formats:
            image_files.extend(glob.glob(os.path.join(self.folder_path, image_format)))
        return image_files

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_MBUTTONDOWN:
            if not self.drawing_box:
                self.start_point = (x, y)
                self.drawing_box = True
            else:
                self.current_box = [self.start_point, (x, y)]
                self.drawing_box = False
                self.drawing_keypoints = True
                self.bounding_boxes.append(self.current_box)
                self.bounding_box_ids.append(len(self.bounding_boxes) - 1)
                self.keypoints.append([])
                self.update_counter()

        elif event == cv2.EVENT_MOUSEMOVE and self.drawing_box:
            self.current_box = [self.start_point, (x, y)]

        elif event == cv2.EVENT_LBUTTONDOWN and self.drawing_keypoints:
            self.keypoints[-1].append((x, y))
            self.update_counter()

    def update_counter(self):
        self.counter -= 1
        if self.counter < 0:
            self.counter = 17
            self.show_save_message = True

    def revert_counter(self):
        self.counter += 1
        if self.counter > 17:
            self.counter = 0
        if self.counter == 17:
            self.show_save_message = False

    def display_images(self, image_files):
        index = 0
        total_images = len(image_files)
        
        if total_images == 0:
            print("No images found in the specified folder.")
            return

        cv2.namedWindow('Image', cv2.WINDOW_AUTOSIZE)
        cv2.setMouseCallback('Image', self.mouse_callback)

        instructions = [
            "Right Ankle (Sag Ayak Bilegi)", "Left Ankle (Sol Ayak Bilegi)", "Right Knee (Sag Diz)", "Left Knee (Sol Diz)", 
            "Right Hip (Sag Kalca)", "Left Hip (Sol Kalca)", "Right Wrist (Sag Bilek)", "Left Wrist (Sol Bilek)", 
            "Right Elbow (Sag Dirsek)", "Left Elbow (Sol Dirsek)", "Right Shoulder (Sag Omuz)", "Left Shoulder (Sol Omuz)", 
            "Right Ear (Sag Kulak)", "Left Ear (Sol Kulak)", "Right Eye (Sag Goz)", "Left Eye (Sol Goz)", 
            "Nose (Burun)", "Bounding box (Sinirlama Kutusu)"
        ]

        while True:
            image_file = image_files[index]
            image = cv2.imread(image_file)
            image_copy = image.copy()
            img_height, img_width = image.shape[:2]

            label_file_path = os.path.join(self.output_folder, os.path.splitext(os.path.basename(image_file))[0] + '.txt')
            saved_bounding_boxes, saved_keypoints = self.label_manager.read_labels(label_file_path, img_width, img_height)

            if image is not None:
                for i, box in enumerate(saved_bounding_boxes):
                    color = self.colors[i % len(self.colors)]
                    cv2.rectangle(image_copy, box[0], box[1], color, 2)
                    for kp in saved_keypoints[i]:
                        if isinstance(kp, tuple):
                            cv2.circle(image_copy, (int(kp[0]), int(kp[1])), 3, color, -1)
                    cv2.putText(image_copy, f'id={i}', (box[0][0], box[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

                for i, box in enumerate(self.bounding_boxes):
                    cv2.rectangle(image_copy, box[0], box[1], self.colors[i % len(self.colors)], 2)
                    for kp in self.keypoints[i]:
                        if isinstance(kp, tuple):
                            cv2.circle(image_copy, (int(kp[0]), int(kp[1])), 3, self.colors[i % len(self.colors)], -1)
                    cv2.putText(image_copy, f'id={self.bounding_box_ids[i]}', (box[0][0], box[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors[i % len(self.colors)], 1, cv2.LINE_AA)
                
                if len(self.current_box) == 2:
                    cv2.rectangle(image_copy, self.current_box[0], self.current_box[1], self.colors[len(self.bounding_boxes) % len(self.colors)], 2)
                for kp in self.keypoints[-1] if self.keypoints else []:
                    if isinstance(kp, tuple):
                        cv2.circle(image_copy, (int(kp[0]), int(kp[1])), 3, self.colors[len(self.bounding_boxes) % len(self.colors)], -1)
                
                current_instruction = f"{self.counter}: {instructions[self.counter]}"
                cv2.putText(image_copy, f"Number of keypoints remaining: {self.counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image_copy, f"Image: {os.path.basename(image_file)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image_copy, current_instruction, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                
                if self.show_save_message:
                    text = "Press the 's' key to save"
                    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                    text_x = (img_width - text_size[0]) // 2
                    cv2.putText(image_copy, text, (text_x, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

                if self.save_message_displayed:
                    text = "Your label is not saved"
                    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                    text_x = (img_width - text_size[0]) // 2
                    cv2.putText(image_copy, text, (text_x, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

                cv2.imshow('Image', image_copy)
                print(f"Displaying {image_file}. Press 'a' for previous, 'd' for next, 's' to save, 'q' to quit, 'z' to add default keypoint, 'r' to undo last action, 'f' to delete bounding box by id.")

                key = cv2.waitKey(1) & 0xFF
                if key == ord('d'):
                    index = (index + 1) % total_images
                    self.bounding_boxes.clear()
                    self.keypoints.clear()
                    self.current_box = []
                    self.drawing_box = False
                    self.drawing_keypoints = False
                    self.start_point = None
                    self.counter = 17
                    self.show_save_message = False
                elif key == ord('a'):
                    index = (index - 1 + total_images) % total_images
                    self.bounding_boxes.clear()
                    self.keypoints.clear()
                    self.current_box = []
                    self.drawing_box = False
                    self.drawing_keypoints = False
                    self.start_point = None
                    self.counter = 17
                    self.show_save_message = False
                elif key == ord('s'):
                    if all(len(kps) == 17 for kps in self.keypoints):
                        self.label_manager.save_bounding_boxes(image_file, self.bounding_boxes, self.keypoints, img_width, img_height)
                        self.bounding_boxes.clear()
                        self.keypoints.clear()
                        self.current_box = []
                        self.drawing_box = False
                        self.drawing_keypoints = False
                        self.start_point = None
                        self.counter = 17
                        self.show_save_message = False
                    else:
                        self.display_save_message()
                elif key == ord('q'):
                    break
                elif key == ord('z') and self.drawing_keypoints:
                    self.keypoints[-1].append((0, 0))
                    self.update_counter()
                elif key == ord('r'):
                    if self.keypoints and self.keypoints[-1]:
                        self.keypoints[-1].pop()
                        if not self.keypoints[-1]:
                            self.show_save_message = False  # Hide save message if no keypoints left
                        self.revert_counter()
                    elif self.bounding_boxes:
                        self.bounding_boxes.pop()
                        self.keypoints.pop()
                        self.current_box = []
                        self.drawing_keypoints = False
                        self.drawing_box = False
                        self.start_point = None
                        self.show_save_message = False  # Hide save message if bounding box removed
                        self.revert_counter()
                elif key == ord('f'):
                    id_to_delete = self.ui_handler.input_id()
                    if id_to_delete is not None:
                        self.label_manager.delete_label(label_file_path, id_to_delete)
                        saved_bounding_boxes, saved_keypoints = self.label_manager.read_labels(label_file_path, img_width, img_height)
                    else:
                        print("Delete operation canceled.")
                
            else:
                print(f"Failed to load image: {image_file}")
        
        cv2.destroyAllWindows()

    def run(self):
        image_files = self.read_images()
        self.display_images(image_files)

    def display_save_message(self):
        self.save_message_displayed = True
        threading.Timer(3.0, self.hide_save_message).start()

    def hide_save_message(self):
        self.save_message_displayed = False
