import os

class LabelManager:
    def __init__(self, output_folder):
        self.output_folder = output_folder

    def read_labels(self, label_file_path, img_width, img_height):
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

    def save_bounding_boxes(self, image_file, bounding_boxes, keypoints, img_width, img_height):
        txt_file_name = os.path.splitext(os.path.basename(image_file))[0] + '.txt'
        txt_file_path = os.path.join(self.output_folder, txt_file_name)

        with open(txt_file_path, 'a') as f:  # Open in append mode
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

    def delete_label(self, label_file_path, id_to_delete):
        if os.path.exists(label_file_path):
            with open(label_file_path, 'r') as f:
                lines = f.readlines()
            with open(label_file_path, 'w') as f:
                for i, line in enumerate(lines):
                    if i != id_to_delete:
                        f.write(line)
            print(f"Deleted bounding box with ID {id_to_delete} from {label_file_path}.")
        else:
            print(f"Label file {label_file_path} not found.")
