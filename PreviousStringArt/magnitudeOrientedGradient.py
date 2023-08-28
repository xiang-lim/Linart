import math

import numpy as np


def magnitude_calculation(tc, bc, lc, rc):
    return ((tc - bc) ** 2 + (rc - lc) ** 2) ** 0.5


def orientation_calculation(tc, bc, lc, rc):
    return math.atan2(tc - bc, rc - lc)


def gradient_calculation(image_array):
    m_o_np_array = []
    magnitude_list = []
    image_array = np.flip(image_array, 0)
    for y in range(1, image_array.shape[0] - 1):
        horizontal_m_o_array = []
        for x in range(1, image_array.shape[1] - 1):
            top_coordinate = int(image_array[y - 1][x])
            bottom_coordinate = int(image_array[y + 1][x])
            left_coordinate = int(image_array[y][x - 1])
            right_coordinate = int(image_array[y][x + 1])
            magnitude = magnitude_calculation(
                top_coordinate,
                bottom_coordinate,
                left_coordinate,
                right_coordinate)
            orientation = orientation_calculation(
                top_coordinate, bottom_coordinate, left_coordinate, right_coordinate)
            horizontal_m_o_array.append((magnitude, orientation, y, x))
            magnitude_list.append(magnitude)
        m_o_np_array.append(horizontal_m_o_array)
    return m_o_np_array, magnitude_list
