import math
from multiprocessing import Pool

import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt
import numpy as np

from Math import cal_gradient, calculate_y_intercept, cal_y_value


class StringArt:
    def __init__(self, image, diameter, point_multiplier):
        self.image = image
        self.resultant_vector = self.convert_img_to_vector()
        self.diameter = diameter
        self.radius = diameter / 2
        self.initial_height = image.shape[0]
        self.initial_width = image.shape[1]
        self.height_offset = self.radius - self.initial_height / 2
        self.width_offset = self.radius - self.initial_width / 2
        self.max_height = self.height_offset * 2 + self.initial_height
        self.max_width = self.width_offset * 2 + self.initial_width
        self.boundary_x = []
        self.boundary_y = []
        self.list_of_boundary = self.determine_360_points(point_multiplier)
        self.string_width_multiplier = 1
        self.string_transparency = 0.4
        self.shadow_weight = 0.5
        self.list_of_current_coord = []
        self.list_of_current_vector = []
        self.list_of_omit = []

    # --------------------------- String Control ---------------------------- #
    def get_string_width(self):
        return 1 + self.string_width_multiplier

    def get_shadow_width(self):
        return (1 + self.string_width_multiplier) * self.shadow_weight

    def add_string_multiplier(self):
        self.string_width_multiplier += 1
        print(self.get_string_width(), self.get_shadow_width())

    # --------------------------- String Control ---------------------------- #

    # ------------------------------ Necessary ------------------------------ #
    def convert_img_to_vector(self):
        print("Converting image into a vector")
        return np.array([np.concatenate(self.image)]).transpose() / 25.5

    def determine_360_points(self, multiplier):
        list_of_boundary = []
        for i in range(0, int(360 * multiplier)):
            y = self.radius * \
                math.sin(i * math.pi / (180 * multiplier)) + self.radius
            x = self.radius * \
                math.cos(i * math.pi / (180 * multiplier)) + self.radius
            list_of_boundary.append((y, x))
            self.boundary_x.append(x)
            self.boundary_y.append(y)
        print("Number of pins: " + str(len(list_of_boundary)))
        return list_of_boundary

    def generate_plot_figure(self, loc, tag):
        list_of_coordinate = []
        for coord1, coord2 in loc:
            list_of_coordinate.append(
                ([coord1[1], coord2[1]], [coord1[0], coord2[0]]))
        plt.figure(
            figsize=(
                (self.diameter // 100) + 1,
                (self.diameter // 100) + 1))
        plt.scatter(self.boundary_x, self.boundary_y, s=1)
        for line in list_of_coordinate:
            plt.plot(
                line[0],
                line[1],
                "k",
                linewidth=self.get_string_width(),
                alpha=self.string_transparency / 2,
                path_effects=[
                    path_effects.SimpleLineShadow(
                        shadow_color="black",
                        linewidth=self.get_shadow_width(),
                        alpha=self.string_transparency / 2,
                    ),
                    path_effects.Normal(),
                ],
            )
        plt.axis("off")
        plt.savefig("Dump/circle_" + tag)
        plt.show()

    # ------------------------------ Necessary ------------------------------ #

    # ---------------------------- Line Equation ---------------------------- #
    def is_straight_line(self, coord1, coord2):
        x1 = "{:.1f}".format(coord1[1])
        x2 = "{:.1f}".format(coord2[1])
        return x1 == x2

    def is_line_on_any_of_the_ranges(
            self,
            upper_bound,
            upper_main,
            lower_main,
            lower_bound,
            value_of_concern):
        return tuple(
            (
                upper_bound
                > value_of_concern + (self.get_string_width() / 2)
                >= upper_main,
                upper_main > value_of_concern >= lower_main,
                lower_main
                > value_of_concern - (self.get_string_width() / 2)
                >= lower_bound,
            )
        )

    def cal_shadow_weight(self, impact):
        return impact * self.shadow_weight * self.string_transparency

    def boundary_weight(self, boundary, value_of_concern, main, lower_main):
        difference = abs(boundary - value_of_concern)
        if main is not None:
            um_above_voc = main - value_of_concern
            if boundary > value_of_concern + 1 and um_above_voc > 0:
                return self.cal_shadow_weight(1 - um_above_voc)
            elif boundary > value_of_concern + 1 and um_above_voc < 0:
                return self.cal_shadow_weight(1)
            elif boundary < value_of_concern + 1 and um_above_voc < 0:
                return self.cal_shadow_weight(difference)
            else:
                return self.cal_shadow_weight(difference - um_above_voc)
        else:
            lm_below_voc = value_of_concern - lower_main
            if boundary < value_of_concern - 1 and lm_below_voc > 0:
                return self.cal_shadow_weight(1 - lm_below_voc)
            elif boundary < value_of_concern - 1 and lm_below_voc < 0:
                return self.cal_shadow_weight(1)
            elif boundary > value_of_concern - 1 and lm_below_voc < 0:
                return self.cal_shadow_weight(difference)
            else:
                return self.cal_shadow_weight(difference - lm_below_voc)

    def line_weight(self, ub, um, lm, lb, bt, voc):
        if bt[0] and bt[1]:
            return (um - voc) * self.string_transparency + (
                self.cal_shadow_weight(voc + 1 - um if ub > voc + 1 else ub - um)
            )
        elif bt[2] and bt[1]:
            return (voc + 1 - lm) * self.string_transparency + (
                self.cal_shadow_weight(lm - voc if lb < voc else lm - lb)
            )
        else:
            return 1 * self.string_transparency

    def weight_of_pixel(
        self,
        upper_bound,
        upper_main,
        lower_main,
        lower_bound,
        boundary_tuple,
        value_of_concern,
    ):
        if boundary_tuple[1]:
            return self.line_weight(
                upper_bound,
                upper_main,
                lower_main,
                lower_bound,
                boundary_tuple,
                value_of_concern,
            )

        elif boundary_tuple[0]:
            return self.boundary_weight(
                upper_bound, value_of_concern, upper_main, None)
        elif boundary_tuple[2]:
            return self.boundary_weight(
                lower_bound, value_of_concern, None, lower_main)
        else:
            return 0

    def calculate_area_of_line(self, point_of_concern, other_point):
        poc_x = point_of_concern[1]
        poc_y = point_of_concern[0]
        op_x = other_point[1]
        op_y = other_point[0]
        # Sanity Checks #
        # Height check
        if (
            (poc_y <= self.height_offset and op_y <= self.height_offset)
            or (
                poc_y >= self.height_offset + self.initial_height
                and op_y >= self.height_offset + self.initial_height
            )
            # Width check
            or (poc_x <= self.width_offset and op_x <= self.width_offset)
            or (
                poc_x >= self.width_offset + self.initial_width
                and op_x >= self.width_offset + self.initial_width
            )
        ):
            self.list_of_omit.append(other_point)
            return tuple(())
        pixel_list = []
        # Pixel calculation #
        if not self.is_straight_line(point_of_concern, other_point):
            gradient = cal_gradient(point_of_concern, other_point)
            c = calculate_y_intercept(point_of_concern, gradient)
            upper_boundary = (
                gradient,
                c + (self.get_string_width() / 2) + (self.get_shadow_width() / 2),
            )
            upper_main_line = (gradient, c + (self.get_string_width() / 2))
            lower_main_line = (gradient, c - (self.get_string_width() / 2))
            lower_boundary = (
                gradient,
                c - (self.get_string_width() / 2) - (self.get_shadow_width() / 2),
            )
            # Normal line #
            for row_num in range(0, self.initial_height):
                for col_num in range(0, self.initial_width):
                    actual_x = col_num + self.width_offset
                    actual_y = row_num + self.height_offset
                    upper_bound_y = cal_y_value(
                        actual_x, upper_boundary[1], upper_boundary[0]
                    )
                    lower_bound_y = cal_y_value(
                        actual_x, lower_boundary[1], lower_boundary[0]
                    )
                    ub_range = (upper_bound_y // 1) + 1
                    lb_range = lower_bound_y // 1
                    if lb_range <= actual_y <= ub_range:

                        upper_main_y = cal_y_value(
                            actual_x, upper_main_line[1], upper_main_line[0]
                        )
                        lower_main_y = cal_y_value(
                            actual_x, lower_main_line[1], lower_main_line[0]
                        )
                        boundary_tuple = self.is_line_on_any_of_the_ranges(
                            ub_range, upper_main_y, lower_main_y, lb_range, actual_y
                        )
                        pixel_list.append(
                            self.weight_of_pixel(
                                upper_bound_y,
                                upper_main_y,
                                lower_main_y,
                                lower_bound_y,
                                boundary_tuple,
                                actual_y,
                            )
                        )

                    else:
                        pixel_list.append(0)
        else:
            # Vertical line
            right_upper_bound = (
                poc_x + (self.get_string_width() / 2) + (self.get_shadow_width() / 2)
            )
            right_upper_main = poc_x + (self.get_string_width() / 2)
            left_lower_main = poc_x - (self.get_string_width() / 2)
            left_lower_bound = (
                poc_x - (self.get_string_width() / 2) - (self.get_shadow_width() / 2)
            )
            for row_num in range(0, self.initial_height):
                for col_num in range(0, self.initial_width):
                    actual_x = col_num + self.width_offset
                    ub_range = (right_upper_bound // 1) + 1
                    lb_range = left_lower_bound // 1
                    if lb_range <= actual_x <= ub_range:
                        boundary_tuple = self.is_line_on_any_of_the_ranges(
                            ub_range,
                            right_upper_main,
                            left_lower_main,
                            lb_range,
                            actual_x,
                        )
                        pixel_list.append(
                            self.weight_of_pixel(
                                right_upper_bound,
                                right_upper_main,
                                left_lower_main,
                                left_lower_bound,
                                boundary_tuple,
                                actual_x,
                            )
                        )
                    else:
                        pixel_list.append(0)
        # Part 1 of greedy
        pixel_vector = np.array([pixel_list]).transpose()
        sum_of_error = (
            np.linalg.norm(
                np.subtract(
                    self.resultant_vector,
                    pixel_vector)) ** 2)
        return tuple((sum_of_error, other_point, pixel_vector))

    # ------------------------ String Art Generation ------------------------ #
    def set_up_area_of_line_calculation(self, point_of_concern):
        list_of_pins = self.list_of_boundary.copy()
        list_of_lines = []
        num_img = 0
        while len(list_of_pins) > 2:
            list_of_vector = []
            list_of_boundary_tuple = []
            # if len(list_of_pins) < len(self.list_of_boundary) * 0.1:
            #     list_of_pins = self.list_of_boundary.copy()
            list_of_pins.remove(point_of_concern)

            for other_point in list_of_pins:
                list_of_boundary_tuple.append((point_of_concern, other_point))
            print(
                "Loading string progress: "
                + str(len(list_of_lines) % 25)
                + " out of 25"
            )
            with Pool(10) as executor:
                results = executor.starmap(
                    self.calculate_area_of_line, list_of_boundary_tuple
                )
            list_of_current_coord = []
            sum_of_error = []
            for result in results:
                if result:
                    sum_of_error.append(result[0])
                    list_of_current_coord.append(result[1])
                    list_of_vector.append(result[2])
            if not sum_of_error:
                break
            # Part 2 of greedy
            min_sum_of_error_index = sum_of_error.index(min(sum_of_error))
            next_point = list_of_current_coord[min_sum_of_error_index]
            self.resultant_vector = np.subtract(
                self.resultant_vector, list_of_vector[min_sum_of_error_index]
            )
            list_of_lines.append((point_of_concern, next_point))
            # End greedy
            point_of_concern = next_point
            if len(list_of_lines) % 25 == 0:
                num_img += 1
                self.generate_plot_figure(list_of_lines, str(num_img))
        self.generate_plot_figure(list_of_lines, "final")

    # ------------------------ String Art Generation ------------------------ #
