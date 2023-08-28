import math

import matplotlib.pyplot as plt
import pandas as pd

from localVariable import attempt_num, variation


def determine_diameter_of_image(height, width):
    return (height**2 + width**2) ** 0.5


def determine_360_points(diameter):
    radius = diameter / 2
    list_coord = []
    for i in range(0, 360):
        y = radius * math.sin(i * math.pi / 180) + radius
        x = radius * math.cos(i * math.pi / 180) + radius
        list_coord.append([x, y])
    return pd.DataFrame(list_coord, columns=["x", "ye"])


def calculate_y_intercept(coordinate, m):
    x1 = coordinate[1]
    y1 = coordinate[0]
    c = m * (-x1) + y1
    return c


def calculate_x_value(y, c, m):
    return (y - c) / m


def cal_euclidean_distance(coord1, coord2):
    x1 = coord1[1]
    y1 = coord1[0]
    x2 = coord2[1]
    y2 = coord2[0]
    return (((y2 - y1) ** 2) + ((x2 - x1) ** 2)) ** 0.5


def calculate_y_point_of_contact_with_circle(radius, coord_of_pixel, radian):
    dist_of_pixel_from_center = cal_euclidean_distance(
        (radius, radius), coord_of_pixel)
    radian_of_pixel_with_respect_to_horizon = math.atan2(
        coord_of_pixel[0], coord_of_pixel[1]
    )
    radian_of_half_sector = math.acos(dist_of_pixel_from_center / radius)
    if math.tan(radian) == math.pi or math.tan(radian) == -math.pi:
        y1 = coord_of_pixel[0]
        x1 = (radius**2 - y1**2) ** 0.5 + radius
        y2 = y1
        x2 = radius - x1
        return (y1, x1), (y2, x2)
    elif math.tan(radian) != 0:
        gradient = -1 / math.tan(radian)
        y1 = (
            radius
            * math.cos(radian_of_pixel_with_respect_to_horizon - radian_of_half_sector)
            + radius
            if coord_of_pixel[0] > radius
            else (-radius)
        )
        c1 = calculate_y_intercept(coord_of_pixel, gradient)
        x1 = calculate_x_value(y1, c1, gradient)
        diff_x = coord_of_pixel[1] - x1
        diff_y = coord_of_pixel[0] - y1
        x2 = x1 + diff_x
        y2 = y1 + diff_y
        return (y1, x1), (y2, x2)
    else:
        x1 = coord_of_pixel[1]
        y1 = (radius**2 - x1**2) ** 0.5 + radius
        x2 = x1
        y2 = radius - y1
        return (y1, x1), (y2, x2)


def determine_closest_coord(width, circle_point_df, coord1, radius):
    small_x = 0
    big_x = width
    for index_df, row_df in circle_point_df.iterrows():
        if row_df["x"] < radius:
            if small_x < row_df.x <= coord1[1]:
                small_x = row_df.x
        else:
            if coord1[1] <= row_df.x < big_x:
                big_x = row_df.x

    coord1_x = big_x if abs(
        coord1[1] -
        small_x) > abs(
        coord1[1] -
        big_x) else small_x
    df_y = circle_point_df[circle_point_df["x"] == coord1_x]

    if len(df_y) > 1:
        coords_y = df_y.ye.to_list()
        coord_y = (
            coords_y[1]
            if abs(coords_y[0] - coord1[0]) > abs(coords_y[1] - coord1[0])
            else coords_y[0]
        )
    else:
        coord_y = df_y.ye

    return tuple((coord_y, coord1_x))


def determine_coordinates_of_line_intercept_with_circle_point(
    diameter, m_o_matrix, circle_point_df, height, width
):
    radius = diameter / 2
    list_of_coord = []
    index = 0
    for row in m_o_matrix:
        print(index)
        index += 1
        for pixel in row:
            if pixel != 0:
                radian = pixel[1]
                coord1, coord2 = calculate_y_point_of_contact_with_circle(
                    radius,
                    (pixel[2] + radius - height / 2, pixel[3] + radius - width / 2),
                    radian,
                )
                coord1 = determine_closest_coord(
                    diameter, circle_point_df, coord1, radius
                )
                coord2 = determine_closest_coord(
                    diameter, circle_point_df, coord2, radius
                )
                list_x = [coord1[1], coord2[1]]
                list_y = [coord1[0], coord2[0]]
                list_of_coord.append((list_x, list_y))
    print("DONE")
    plt.figure(figsize=(10, 10))
    for line in list_of_coord:
        plt.plot(line[0], line[1], linewidth=1, alpha=0.01)
    plt.savefig(
        "Attempts/Attempt"
        + attempt_num
        + "/Variation_"
        + variation
        + "/String_Art_Attempt_"
        + attempt_num
    )
    plt.show()


def visualize_string_art_v2(magnitude_orientation_matrix):
    height = len(magnitude_orientation_matrix)
    width = len(magnitude_orientation_matrix[0])
    diameter_of_image = determine_diameter_of_image(height, width)
    circle_coord_df = determine_360_points(diameter_of_image)
    print(circle_coord_df)
    determine_coordinates_of_line_intercept_with_circle_point(
        diameter_of_image, magnitude_orientation_matrix, circle_coord_df, height, width)
    # plt.figure(figsize=(10,10))
    # for line in list_of_lines:
    #     print(line)
    #     plt.plot(line[0], line[1], linewidth=1, alpha=0.01)
