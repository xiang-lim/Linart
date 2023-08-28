import itertools
import math
from concurrent.futures import ProcessPoolExecutor
from multiprocessing.dummy import Pool

import matplotlib.pyplot as plt
import numpy as np

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
        self.string_weight = 5
        self.string_thickness = 1  # Unit in pixel
        self.circular_coord = self.determine_360_points()
        self.max_workers = 6
        self.number_of_thread = 40
        self.apvd = {}

    def determine_360_points(self):
        list_coord = []
        for i in range(0, 360, 5):
            y = self.radius * math.sin(i * math.pi / 180) + self.radius
            x = self.radius * math.cos(i * math.pi / 180) + self.radius
            list_coord.append((y, x))
        return list_coord

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
                        if col_num <= straight_value_x < col_num + 1.5:
                            if straight_value_x // 1 == col_num:
                                vector_of_string.append(
                                    (
                                        straight_value_x
                                        + self.string_thickness / 2
                                        - col_num
                                    )
                                    * self.string_weight
                                )
                            else:
                                vector_of_string.append(
                                    (
                                        (
                                            col_num
                                            - (
                                                straight_value_x
                                                - self.string_thickness / 2
                                            )
                                        )
                                        + 1
                                    )
                                    * self.string_weight
                                )
                            continue
                        vector_of_string.append(0)
                        continue
                    elif is_flat:
                        y_value = cal_y_value(col_num, c, gradient)
                        if row_num <= y_value < row_num + 1.5:
                            if y_value // 1 == row_num:
                                vector_of_string.append(
                                    (y_value + self.string_thickness / 2 - row_num) * self.string_weight)
                            else:
                                vector_of_string.append(
                                    (
                                        (
                                            row_num
                                            - (y_value - self.string_thickness / 2)
                                        )
                                        + 1
                                    )
                                    * self.string_weight
                                )

                            continue
                        vector_of_string.append(0)
                        continue
                    else:
                        y_value = cal_y_value(col_num, c, gradient)
                        if row_num <= y_value < row_num + 1.5:
                            if y_value // 1 == row_num:
                                vector_of_string.append(
                                    (y_value + self.string_thickness / 2 - row_num) * self.string_weight)
                            else:
                                vector_of_string.append(
                                    (
                                        (
                                            row_num
                                            - (y_value - self.string_thickness / 2)
                                        )
                                        + 1
                                    )
                                    * self.string_weight
                                )
                            continue
                        vector_of_string.append(0)
                        continue
                vector_of_string.append(0)
        if len(vector_of_string) != 409600:
            print("WARNING")
        return vector_of_string

    def cal_one_vs_all_point(self, input_tuple):
        other_point_index = input_tuple[0]
        point_of_concern = input_tuple[1]
        other_point = self.circular_coord[other_point_index]
        return (
            other_point,
            self.cal_vector_of_lines_on_image(point_of_concern, other_point),
        )

    def cal_each_point_vectors(self):
        num_of_points_considered = 0
        vector_dictionary = {}
        pinV = []
        for i in range(0, len(self.circular_coord)):
            point_of_concern = self.circular_coord[i]
            num_of_points_considered += 1
            print(
                "Calculating "
                + str(i)
                + " of "
                + str(len(self.circular_coord))
                + " points vector"
            )
            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                results = list(
                    executor.map(
                        self.cal_one_vs_all_point, zip(
                            range(
                                num_of_points_considered, len(
                                    self.circular_coord)), itertools.repeat(point_of_concern), ), ))
            for result in results:
                vector_dictionary[(point_of_concern, result[0])] = result[1]
                vector_dictionary[(result[0], point_of_concern)] = result[1]
                pinV.append(result[1])
        self.apvd = vector_dictionary

    def convert_img_to_vector(self):
        print("Converting image into a vector")
        print(self.image.shape)
        return np.concatenate(np.array(self.image))

    def calculate_resultant_vector(self, input_tuple):
        other_point_index = input_tuple[0]
        point_of_concern = input_tuple[1]
        min_value = input_tuple[2]
        max_value = input_tuple[3]
        other_point = self.circular_coord[other_point_index]
        if other_point != point_of_concern:
            current_resultant_vector = self.resultant_vector.copy()
            current_vector = self.apvd[(point_of_concern, other_point)]
            weight = []
            for v1 in current_resultant_vector:
                weight.append((v1 - min_value) / (max_value / min_value))
            weight_based = np.multiply(current_vector, weight)
            resultant_vector = np.subtract(
                current_resultant_vector, current_vector)

            sum_of_errors = sum(
                np.subtract(
                    current_resultant_vector,
                    weight_based))
            return ((point_of_concern, other_point),
                    sum_of_errors, resultant_vector)
        return ()

    def calculate_best_possible_line(self, point_of_concern):
        print("Calculating best possible line, sum of error: " +
              str(self.sum_of_error()))
        all_point_sum_of_errors = {}
        resultant_vector_dict = {}
        max_value = max(self.resultant_vector)
        min_value = min(self.resultant_vector)
        with Pool() as executor:
            results = executor.map(
                self.calculate_resultant_vector,
                zip(
                    range(0, len(self.circular_coord)),
                    itertools.repeat(point_of_concern),
                    itertools.repeat(min_value),
                    itertools.repeat(max_value),
                ),
            )

        for result in results:
            if result:
                coordinate = result[0]
                other_point = result[0][1]
                resultant_vector_dict[other_point] = result[2]
                all_point_sum_of_errors[coordinate] = result[1]

        all_point_sum_of_errors = {
            k: v
            for k, v in sorted(
                all_point_sum_of_errors.items(), key=lambda item: item[1]
            )
        }
        point = next(iter(all_point_sum_of_errors))

        self.resultant_vector = resultant_vector_dict[point[1]]

        return point

    def sum_of_error(self):
        sum_of_error = 0
        for scalar in self.resultant_vector:
            sum_of_error += scalar
        return sum_of_error

    def is_complete(self):

        return self.sum_of_error() < 0

    def aggregate_lines(self):
        print("Aggregate_lines")
        list_of_line_combination = []
        next_coordinates = self.circular_coord[0]
        while not self.is_complete():
            best_possible_line = self.calculate_best_possible_line(
                next_coordinates)
            list_of_line_combination.append(best_possible_line)
            next_coordinates = best_possible_line[1]
            print(next_coordinates)
            list_of_coordinate = []
            if len(list_of_line_combination) % 25 == 0:
                for pair_of_combination in list_of_line_combination:
                    coord1 = pair_of_combination[0]
                    coord2 = pair_of_combination[1]
                    list_of_coordinate.append(
                        ([coord1[1], coord2[1]], [coord1[0], coord2[0]])
                    )
                plt.figure(
                    figsize=(
                        (self.diameter // 100) + 3,
                        (self.diameter // 100) + 3))
                for line in list_of_coordinate:
                    plt.plot(line[0], line[1], linewidth=1, alpha=0.01)
                plt.show()
        return list_of_line_combination

    def generate_string_art(self):
        self.cal_each_point_vectors()
        list_of_line_combination = self.aggregate_lines()
        list_of_coordinate = []
        for pair_of_combination in list_of_line_combination:
            coord1 = pair_of_combination[0]
            coord2 = pair_of_combination[1]
            list_of_coordinate.append(
                ([coord1[1], coord2[1]], [coord1[0], coord2[0]]))
        plt.figure(
            figsize=(
                (self.diameter // 100) + 3,
                (self.diameter // 100) + 3))
        for line in list_of_coordinate:
            plt.plot(line[0], line[1], linewidth=1, alpha=0.01)
        plt.savefig("Test")

        plt.show()
