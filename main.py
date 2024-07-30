from image_processor import ImageProcessor
from ui_handler import UIHandler

def main():
    folder_path = 'data/images/train'
    output_folder = 'data/labels/train'

    ui_handler = UIHandler()
    image_processor = ImageProcessor(folder_path, output_folder, ui_handler)
    
    image_processor.run()

if __name__ == "__main__":
    main()
