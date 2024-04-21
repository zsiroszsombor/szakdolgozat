import os
from PIL import Image

def is_mostly_white(image_path, threshold=200):
    with Image.open(image_path) as img:
        grayscale_img = img.convert('L')
        histogram = grayscale_img.histogram()
        total_pixels = img.width * img.height
        white_pixels = sum(histogram[i] for i in range(threshold, 256))
        return (white_pixels / total_pixels) > 0.95

def remove_white_images(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.tif'):
            image_path = os.path.join(directory, filename)
            if is_mostly_white(image_path):
                os.remove(image_path)
                print(f"Removed: {filename}")


remove_white_images("train/image")