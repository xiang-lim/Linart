import math

from matplotlib import pyplot as plt

from localVariable import attempt_num, variation


def calculate_y_intercept(coordinate, m):
    x1 = coordinate[1]
    y1 = coordinate[0]
    c = m * (-x1) + y1
    return c


def visualize_string_art(magnitude_orientation_matrix):
    list_of_lines = []
    for row in magnitude_orientation_matrix:
        for pixel in row:
            if not pixel == 0:
                angle = pixel[1]
                gradient = (math.tan(angle) if math.tan(
                    angle) == 0 else -1 / math.tan(angle))
                c = calculate_y_intercept((pixel[2], pixel[3]), gradient)
                list_of_lines.append(([pixel[3], 0], [pixel[2], c]))
    plt.figure(figsize=(7, 7))
    plt.axis([0, 640, 0, 640])
    for line in list_of_lines:
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
