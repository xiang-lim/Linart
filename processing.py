import pandas as pd
from matplotlib import pyplot as plt

from localVariable import attempt_num, variation


def m_o_threshold_filter(magnitude_orientation_maxtrix, magnitude_array):
    m_df = pd.DataFrame(magnitude_array, columns=["magnitude"])
    magnitude_quintile = m_df.quantile(0.916)
    magnitude_quintile_max = m_df.quantile(1)
    map_of_affected_points_horizontal = []
    map_of_affected_points_vertical = []
    vertical_index = 0
    for i in magnitude_orientation_maxtrix:
        horizontal_index = 0
        for j in i:
            if (
                not j[0] >= magnitude_quintile.magnitude
            ):
                i[horizontal_index] = 0
            else:
                map_of_affected_points_vertical.append(vertical_index)
                map_of_affected_points_horizontal.append(horizontal_index)
            horizontal_index += 1
        vertical_index += 1
    return (
        magnitude_orientation_maxtrix,
        map_of_affected_points_horizontal,
        map_of_affected_points_vertical,
    )


def visualize_plot_points(x_axis, y_axis):
    plt.figure(figsize=(7, 7))
    plt.scatter(x_axis, y_axis, s=2)
    plt.xticks(rotation="vertical")
    plt.savefig("Attempts/Attempt"+attempt_num+"/Variation_"+variation+"/Plot_Point_Attempt_"+attempt_num)
    plt.show()
