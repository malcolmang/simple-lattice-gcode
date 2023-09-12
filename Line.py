import math


class Line:
    def __init__(self, start, end):
        self.start = start[:]
        self.end = end[:]
        self.next_line = None

    def generate_gcode(self, e):
        # should already be at start from previous line. goes to next line's start position
        # returns absolute extruder positon as well as gcode for convenience
        if (self.next_line is None):
            # last line in layer
            e_new =  e + math.dist(self.start, self.end)
            return e_new, f"G1 X{self.end[0]:.4f} Y{self.end[1]:.4f} E{e_new:.4f}\n"
        else:
            e_new = e + math.dist(self.start, self.end) + math.dist(self.end, self.next_line.start)
            return e_new, f"G1 X{self.end[0]:.4f} Y{self.end[1]:.4f} E{e + math.dist(self.start, self.end):.4f}\nG1 X{self.next_line.start[0]:.4f} Y{self.next_line.start[1]:.4f} E{e_new:.4f}\n"

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_next_line(self, nextline):
        self.next_line = nextline

    def get_next_line(self):
        pass

    def flip_line(self):
        self.start, self.end = self.end, self.start

    def distance(self, point_1, point_2):
        return math.dist(point_1, point_2)

