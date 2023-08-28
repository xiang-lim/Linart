def cal_diameter_of_image(height, width):
    return (height**2 + width**2) ** 0.5


def calculate_y_intercept(coordinate, m):
    x1 = coordinate[1]
    y1 = coordinate[0]
    c = m * (-x1) + y1
    return c


def cal_y_value(x, c, m):
    return m * x + c


def calculate_x_value(y, c, m):
    return (y - c) / m


def cal_euclidean_distance(coord1, coord2):
    x1 = coord1[1]
    y1 = coord1[0]
    x2 = coord2[1]
    y2 = coord2[0]
    return (((y2 - y1) ** 2) + ((x2 - x1) ** 2)) ** 0.5


def is_straight_line(coord1, coord2):
    x1 = coord1[1]
    x2 = coord2[1]
    return (x1 - x2) == 0


def cal_gradient(coord1, coord2):
    x1 = coord1[1]
    y1 = coord1[0]
    x2 = coord2[1]
    y2 = coord2[0]
    return (y1 - y2) / (x1 - x2)
