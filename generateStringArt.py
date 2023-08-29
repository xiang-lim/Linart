import itertools
import math
import multiprocessing
from multiprocessing import Pool
import numpy as np
from matplotlib import pyplot as plt

from Math import cal_gradient, calculate_y_intercept, cal_y_value, is_straight_line


class StringArt:
    def __init__(self, image, diameter):
        self.image = image
        self.image_vector = self.convert_img_to_vector()
        self.resultant_vector = self.image_vector
        self.diameter = diameter
        self.radius = diameter / 2
        self.initial_height = image.shape[0]
        self.initial_width = image.shape[1]
        self.height_offset = self.radius - self.initial_height / 2
        self.width_offset = self.radius - self.initial_width / 2
        self.max_height = self.height_offset * 2 + self.initial_height
        self.max_width = self.width_offset * 2 + self.initial_width
        self.string_weight = 0.2
        self.string_thickness = 1  # Unit in pixel
        self.initial_circular_coord = self.determine_360_points()
        self.circular_coord = self.determine_360_points()
        self.max_workers = 10
        self.current_A_coord = []
        self.acd = {}
        self.max_x_vector = []

    def greedy_algorithm(self, A):
        print(A.shape)
        x_vector = np.dot(np.linalg.pinv(A), self.resultant_vector)
        x_vector = x_vector.tolist()
        return x_vector.index(max(x_vector))

    def determine_360_points(self):
        list_coord = []
        for i in range(0, 360, 15):
            y = self.radius * math.sin(i * math.pi / 180) + self.radius
            x = self.radius * math.cos(i * math.pi / 180) + self.radius
            list_coord.append((y, x))
        return list_coord

    def determine_line_pixel_value(self, lower_bound, value, vector_of_string):
        if lower_bound <= value < lower_bound + 1.5:
            if value // 1 == lower_bound:
                vector_of_string.append(
                    ((value - lower_bound) + (self.string_thickness / 2))
                    * self.string_weight
                )
            else:
                vector_of_string.append(
                    ((lower_bound - (value - (self.string_thickness / 2))) + 1)
                    * self.string_weight
                )
            return
        vector_of_string.append(0)
        return

    def cal_vector_of_lines_on_image(self, point_of_concern, other_point):
        straight_value_x = 0
        c = 0
        gradient = 0
        if is_straight_line(point_of_concern, other_point):
            straight_value_x = point_of_concern[1]
            cal_max_y = self.diameter
        else:
            gradient = cal_gradient(point_of_concern, other_point)
            c = calculate_y_intercept(point_of_concern, gradient)
            cal_max_y = (
                cal_y_value(
                    self.width_offset,
                    c,
                    gradient) if cal_y_value(
                    self.width_offset,
                    c,
                    gradient) > cal_y_value(
                    self.max_width -
                    self.width_offset,
                    c,
                    gradient) else cal_y_value(
                    self.max_width -
                    self.width_offset,
                    c,
                    gradient))
        vector_of_string = []
        is_flat = gradient == 0
        for row_num in range(
                int((self.max_height - self.height_offset) // 1),
                int(self.height_offset // 1),
                -1,
        ):
            is_skip = row_num > cal_max_y
            for col_num in range(
                    int(self.width_offset // 1),
                    int((self.max_width - self.width_offset) // 1),
            ):
                if not is_skip:
                    if is_straight_line(point_of_concern, other_point):
                        self.determine_line_pixel_value(
                            col_num, straight_value_x, vector_of_string
                        )
                        continue
                    elif is_flat:
                        y_value = cal_y_value(col_num, c, gradient)
                        self.determine_line_pixel_value(
                            row_num, y_value, vector_of_string
                        )
                        continue
                    else:
                        y_value = cal_y_value(col_num, c, gradient)
                        self.determine_line_pixel_value(
                            row_num, y_value, vector_of_string
                        )
                        continue
                vector_of_string.append(0)
        return vector_of_string

    def cal_one_vs_all_point(self, other_point_index, point_of_concern):
        other_point = self.circular_coord[other_point_index]
        if other_point != point_of_concern:
            return (
                other_point,
                self.cal_vector_of_lines_on_image(point_of_concern, other_point),
            )

    def cal_each_point_vectors(self, point_of_concern):
        matrix_of_lines = []
        print("Initialize matrix")
        with Pool(processes=self.max_workers) as executor:
            results = executor.starmap(
                self.cal_one_vs_all_point, zip(
                    range(
                        0, len(self.circular_coord)), itertools.repeat(point_of_concern), ), )
        acd = {}
        current_coord = []
        for result in results:
            if result:
                matrix_of_lines.append(np.array([result[1]]).transpose())
                acd[len(current_coord)] = np.array([result[1]]).transpose()
                current_coord.append(result[0])
        print("Returning matrix")
        self.current_A_coord = current_coord
        self.acd = acd
        matrix = np.array([])
        for index in range(0, len(matrix_of_lines)):
            if index == 0:
                matrix = matrix_of_lines[0]
            else:
                matrix += matrix
        print(min(matrix))
        return np.concatenate(matrix_of_lines, axis=1)

    def convert_img_to_vector(self):
        print("Converting image into a vector")
        return np.array([np.concatenate(self.image)]).transpose()/25.5

    def organize_points_calculation(self, point_of_concern):
        list_of_coordinates = []
        previous_coord = None
        for i in range(0, 25):
            is_matrix_not_empty=True
            a = 0
            while is_matrix_not_empty:
                self.circular_coord = self.initial_circular_coord.copy()
                self.circular_coord.remove(point_of_concern)
                if previous_coord is not None:
                    self.circular_coord.remove(previous_coord)
                matrix_a = self.cal_each_point_vectors(point_of_concern)
                coord_index = self.greedy_algorithm(matrix_a)
                previous_coord = point_of_concern
                next_coord = self.current_A_coord[coord_index]
                print((point_of_concern, next_coord))
                list_of_coordinates.append((point_of_concern, next_coord))
                point_of_concern = next_coord
                self.resultant_vector = np.subtract(self.resultant_vector, self.acd[coord_index])
                is_matrix_not_empty = matrix_a.shape[1] > a
                a+=1
            list_of_coordinate = []
            for coord1, coord2 in list_of_coordinates:
                list_of_coordinate.append(
                    ([coord1[1], coord2[1]], [coord1[0], coord2[0]]))
            plt.figure(
                figsize=(
                    (self.diameter // 100) + 3,
                    (self.diameter // 100) + 3))
            for line in list_of_coordinate:
                plt.plot(line[0], line[1], 'k', linewidth=1, alpha=0.1)
            plt.savefig("Dump/"+str(i))
            plt.show()
        return list_of_coordinates

    def generate_string_art(self):
        list_of_coordinates = self.organize_points_calculation(self.circular_coord[1])
        print(list_of_coordinates)
        list_of_coordinate = []
        for pair_of_combination in list_of_coordinates:
            coord1 = pair_of_combination[0]
            coord2 = pair_of_combination[1]
            list_of_coordinate.append(
                ([coord1[1], coord2[1]], [coord1[0], coord2[0]]))
        plt.figure(
            figsize=(
                (self.diameter // 100) + 3,
                (self.diameter // 100) + 3))
        for line in list_of_coordinate:
            plt.plot(line[0], line[1], linewidth=1, alpha=0.1)
        plt.savefig("Test")
        plt.show()
