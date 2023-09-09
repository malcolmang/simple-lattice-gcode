class Line:
    def __init__(self, start, end):
        self.start = start[:]
        self.end = end[:]

    def generate_gcode(self):
        pass

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_next_line(self):
        pass

    def get_next_line(self):
        pass