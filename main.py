import math
import os
import re

import matplotlib.image as mpimg
from PIL import Image


def convert_to_greyscale(this_file_path: str, this_file_name: str):
    greyscale_dir = "Greyscale/"
    new_file_loc = greyscale_dir + this_file_name
    image = Image.open(this_file_path).convert("L")
    image.save(new_file_loc)
    return new_file_loc


def magnitude_calculation(tc, bc, lc, rc):
    return ((tc - bc) ** 2 + (lc - rc) ** 2) ** 0.5


def orientation_calculation(tc, bc, lc, rc):
    return math.atan2(tc - bc, lc - rc)


def gradient_calculation(image_array):
    m_o_np_array = []
    magnitude_array = []
    for y in range(1, image_array.shape[0] - 1):
        horizontal_m_o_array = []
        for x in range(1, image_array.shape[1] - 1):
            top_coordinate = int(image_array[y - 1][x])
            bottom_coordinate = int(image_array[y + 1][x])
            left_coordinate = int(image_array[y][x - 1])
            right_coordinate = int(image_array[y][x + 1])
            magnitude = magnitude_calculation(top_coordinate, bottom_coordinate, left_coordinate, right_coordinate)
            orientation = orientation_calculation(top_coordinate, bottom_coordinate, left_coordinate, right_coordinate)
            horizontal_m_o_array.append((magnitude, orientation))
            magnitude_array.append(magnitude)
        m_o_np_array.append(horizontal_m_o_array)
    return m_o_np_array, magnitude_array


if __name__ == "__main__":
    directory_name = "Input"
    greyscale_dir_list = []
    for file_name in os.listdir(directory_name):
        if re.search(r"\.(jpeg|jpg|png)$", file_name):
            file_path = directory_name + "/" + file_name
            greyscale_dir_list.append(convert_to_greyscale(file_path, file_name))

    for greyscale_image in greyscale_dir_list:
        img = mpimg.imread(greyscale_image)
        m_o_array, m_array = gradient_calculation(img)
