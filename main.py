import os
import re

import matplotlib.image as mpimg
import numpy as np
from PIL import Image

from Math import cal_diameter_of_image
from generateStringArt import StringArt


def convert_to_greyscale():
    directory_name = "Input"
    greyscale_dir = "Greyscale/"
    for file_name in os.listdir(directory_name):
        if re.search(r"\.(jpeg|jpg|png)$", file_name):
            file_path = directory_name + "/" + file_name
            new_file_loc = greyscale_dir + file_name
            image = Image.open(file_path).convert("L")
            image.save(new_file_loc)
            greyscale_dir_list.append(new_file_loc)


def determine_diameter_of_image(height, width):
    return (height**2 + width**2) ** 0.5


if __name__ == "__main__":
    greyscale_dir_list = []
    convert_to_greyscale()
    for greyscale_image in greyscale_dir_list:
        img = mpimg.imread(greyscale_image)
        img = np.flip(img, 0)
        diameter = cal_diameter_of_image(img.shape[0], img.shape[1])
        string_art = StringArt(img, diameter)
        string_art.generate_string_art()
