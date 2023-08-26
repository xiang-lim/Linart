import os
import re

import matplotlib.image as mpimg
from PIL import Image

from magnitudeOrientedGradient import gradient_calculation
from processing import visualize_plot_points, m_o_threshold_filter
from stringArt import visualize_string_art


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


if __name__ == "__main__":

    greyscale_dir_list = []
    convert_to_greyscale()
    for greyscale_image in greyscale_dir_list:
        img = mpimg.imread(greyscale_image)
        m_o_matrix, m_array = gradient_calculation(img)
        m_o_matrix_filtered, affected_point_h, affected_point_v = m_o_threshold_filter(
            m_o_matrix, m_array)
        visualize_plot_points(affected_point_h, affected_point_v)
        visualize_string_art(m_o_matrix_filtered)
