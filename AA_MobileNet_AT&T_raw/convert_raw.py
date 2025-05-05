import os
import cv2
import numpy as np

def convert_to_raw(input_dir='data/att_faces', output_file='att_faces.raw'):
    raw_data = []
    for person in os.listdir(input_dir):
        for img_file in os.listdir(os.path.join(input_dir, person)):
            img_path = os.path.join(input_dir, person, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (64, 64))
            _, img_bin = cv2.threshold(img, 128, 1, cv2.THRESH_BINARY)
            bits = np.packbits(img_bin.reshape(-1))
            raw_data.append(bits.tobytes())
    with open(output_file, 'wb') as f:
        for data in raw_data:
            f.write(data)

if __name__ == '__main__':
    convert_to_raw()