import math

import numpy as np
import matplotlib.pyplot as plt
from Line import Line

class Layer:
    def __init__(self, bounds, spacing, rotation = 0):
        # initialise list of lines
        self.spacing = spacing
        self.bounds = bounds
        self.rotation = rotation
        self.line_list = self.generate_lines(rotation, bounds, spacing)

    def generate_lines(self, rotation, bounds, spacing):
        # always starts on the vertical line
        start_point, end_point = self.calculate_start_end(rotation, bounds, spacing)
        line_list = []
        while (True):
            if (bounds.valid_point(start_point) and bounds.valid_point(end_point)):
                line_list.append(Line(start_point, end_point))
            else:
                break
            start_point = self.step_start(rotation, bounds, spacing, start_point)
            end_point = self.step_end(rotation, bounds, spacing, end_point)
        return line_list


    def step_start(self, rotation, bounds, spacing, start_point, half = False):
        start_point_return = start_point[:]
        if rotation == 0 or rotation % 180 == 0:
            start_point_return[1] += spacing
        elif rotation % 90 == 0:
            start_point_return[0] += spacing
        elif rotation % 180 > 90:
            # diagonal lines going downward - climb upward then to the right
            horizontal_climb = spacing / math.sin(math.radians(rotation % 180))
            vertical_climb = spacing / math.sin(math.radians(abs(90 - (rotation % 180))))
            if half:
                horizontal_climb /= 2
                vertical_climb /= 2
            # still within vertical bounds
            if (start_point[1] != bounds.get_c2()[1]):
                # if next step will be out of bounds
                if (start_point[1] + vertical_climb > bounds.get_c2()[1]):
                    height_delta = start_point[1] + vertical_climb - bounds.get_c2()[1]
                    horizontal_delta = height_delta / math.tan(math.radians(abs(90 - rotation % 90)))
                    start_point_return = [start_point[0] + horizontal_delta, bounds.get_c2()[1]]
                else:
                    start_point_return[1] += vertical_climb
            else:
                start_point_return[0] += horizontal_climb
        else:
            # diagonal lines going upward - climb upward then to the left
            horizontal_climb = - spacing / math.sin(math.radians(rotation % 180))
            vertical_climb = spacing / math.sin(math.radians(abs(90 - (rotation % 180))))
            if half:
                horizontal_climb /= 2
                vertical_climb /= 2
            # still within vertical bounds
            if (start_point[1] != bounds.get_c2()[1]):
                # if next step will be out of bounds
                if (start_point[1] + vertical_climb > bounds.get_c2()[1]):
                    height_delta = start_point[1] + vertical_climb - bounds.get_c2()[1]
                    horizontal_delta = height_delta * math.tan(math.radians(abs(90 - rotation % 90)))
                    start_point_return = [start_point[0] - horizontal_delta, bounds.get_c2()[1]]
                else:
                    start_point_return[1] += vertical_climb
            else:
                start_point_return[0] += horizontal_climb

        return start_point_return


    def step_end(self, rotation, bounds, spacing, end_point, half = False):
        end_point_return = end_point[:]
        if rotation == 0 or rotation % 180 == 0:
            end_point_return[1] += spacing
        elif rotation % 90 == 0:
            end_point_return[0] += spacing
        elif rotation % 180 > 90:
            # diagonal lines going downward - climb right then upward
            horizontal_climb = spacing / math.sin(math.radians(rotation % 180))
            vertical_climb = spacing / math.sin(math.radians(abs(90 - (rotation % 180))))
            if half:
                horizontal_climb /= 2
                vertical_climb /= 2
            # still within horizontal bounds
            if (end_point[0] != bounds.get_c2()[0]):
                # if next step will be out of bounds
                if (end_point[0] + horizontal_climb > bounds.get_c2()[0]):
                    horizontal_delta = end_point[0] + horizontal_climb - bounds.get_c2()[0]
                    vertical_delta = horizontal_delta / math.tan(math.radians(abs(rotation % 90)))
                    end_point_return = [bounds.get_c2()[0], end_point[1] + vertical_delta]
                else:
                    end_point_return[0] += horizontal_climb
            else:
                end_point_return[1] += vertical_climb
        else:
            # diagonal lines going upward - climb left then upward
            horizontal_climb = -spacing / math.sin(math.radians(rotation % 180))
            vertical_climb = spacing / math.sin(math.radians(abs(90 - (rotation % 180))))
            if half:
                horizontal_climb /= 2
                vertical_climb /= 2
            # still within horizontal bounds
            if (end_point[0] != bounds.get_c1()[0]):
                # if next step will be out of bounds
                if (end_point[0] + horizontal_climb < bounds.get_c1()[0]):
                    horizontal_delta = abs(bounds.get_c1()[0] - (end_point[0] + horizontal_climb))
                    vertical_delta = horizontal_delta * math.tan(math.radians(abs(rotation % 90)))
                    end_point_return = [bounds.get_c1()[0], end_point[1] + vertical_delta]
                else:
                    end_point_return[0] += horizontal_climb
            else:
                end_point_return[1] += vertical_climb
        return end_point_return




    def calculate_start_end(self, rotation, bounds, spacing):
        starting_coordinate = list(bounds.get_c1())
        ending_coordinate = list(bounds.get_c2())

        # if horizontal
        if rotation == 0 or rotation % 180 == 0:
            current_coordinate_start = starting_coordinate[:]
            current_coordinate_end = [ending_coordinate[0], starting_coordinate[1]]

        #if vertical
        elif rotation % 90 == 0:
            current_coordinate_start = starting_coordinate[:]
            current_coordinate_end = [starting_coordinate[0], ending_coordinate[1]]

        #if negative gradient (sloping down), start on the bottom left corner
        elif rotation % 180 > 90:
            bottom_left_corner = starting_coordinate[:]
            current_coordinate_start = self.step_start(rotation, bounds, spacing, bottom_left_corner, True)
            current_coordinate_end = self.step_end(rotation, bounds, spacing, bottom_left_corner, True)

        #if positive gradient (sloping up), start on the bottom right corner
        else:
            bottom_right_corner = [ending_coordinate[0], starting_coordinate[1]]
            current_coordinate_start = self.step_start(rotation, bounds, spacing, bottom_right_corner, True)
            current_coordinate_end = self.step_end(rotation, bounds, spacing, bottom_right_corner, True)

        return current_coordinate_start, current_coordinate_end

    def plot_points(self):
        for line in self.line_list:
            x = []
            y = []
            x.append(line.get_start()[0])
            y.append(line.get_start()[1])

            x.append(line.get_end()[0])
            y.append(line.get_end()[1])
            plt.xlim([self.bounds.get_c1()[0] - 20, self.bounds.get_c2()[0] + 20])
            plt.ylim([self.bounds.get_c1()[1] - 20, self.bounds.get_c2()[1] + 20])
            plt.plot(x, y, marker="o")


    def generate_gcode(self):
        pass

    def get_rotation(self):
        pass

    def set_next_layer(self):
        pass

    def get_next_layer(self):
        pass
