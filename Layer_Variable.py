import math
import matplotlib.pyplot as plt
from Line import Line

class LayerVariableSpacing:
    def __init__(self, bounds, spacing_list, layer_height, rotation = 0):
        # initialise list of lines
        # spacing_list is a list of spaces
        self.spacing_list = spacing_list
        self.bounds = bounds
        self.rotation = rotation
        self.layer_height = layer_height
        self.line_list = self.generate_lines(rotation, bounds, spacing_list)

    def generate_lines(self, rotation, bounds, spacing_list):
        # always starts on the vertical line
        # iterates through spacing list
        currindex = 0
        start_point, end_point = self.calculate_start_end(rotation, bounds, spacing_list[currindex])
        line_list = []
        while (True):
            if (bounds.valid_point(start_point) and bounds.valid_point(end_point)):
                line_list.append(Line(start_point, end_point))
            else:
                break
            currindex = min(len(spacing_list) - 1, currindex)
            start_point = self.step_start(rotation, bounds, spacing_list[currindex], start_point)
            end_point = self.step_end(rotation, bounds, spacing_list[currindex], end_point)
            currindex += 1
        line_list = self.stitch_lines(line_list)
        return line_list

    def stitch_lines(self, line_list):
        for i, line in enumerate(line_list):
            if i % 2 == 1:
                line.flip_line()

        for i, line in enumerate(line_list):
            if (i != len(line_list) - 1):
                line.set_next_line(line_list[i+1])
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
        plt.clf()
        for line in self.line_list:
            x = []
            y = []
            x.append(line.get_start()[0])
            y.append(line.get_start()[1])
            x.append(line.get_end()[0])
            y.append(line.get_end()[1])

            plt.xlim([self.bounds.get_c1()[0] - 20, self.bounds.get_c2()[0] + 20])
            plt.ylim([self.bounds.get_c1()[1] - 20, self.bounds.get_c2()[1] + 20])
            plt.title(f"Layer at z = {self.layer_height:.3f}")
            plt.plot(x, y, marker="o")



    def generate_gcode(self, feed_rate, extruderpos = 0):
        header = f"G1 Z{self.layer_height:.4f} F{feed_rate:.4f}\nG1 X{self.line_list[0].start[0]:.4f} Y{self.line_list[0].start[1]:.4f} F{feed_rate:.4f}\n"
        bufferstring = header
        extruderpos_new = extruderpos
        for line in self.line_list:
            extruderpos_new, gcode = line.generate_gcode(extruderpos_new)
            bufferstring += gcode
        return extruderpos_new, bufferstring

    def get_rotation(self):
        pass

    def set_next_layer(self):
        pass

    def get_next_layer(self):
        pass
