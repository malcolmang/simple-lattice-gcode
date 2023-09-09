class Bounds:
    # Should be opposite corners
    def __init__(self, corner1, corner2):
        #flip rectangle to make valid if coordinates are reversed
        if (corner2[0] < corner1[0]):
            corner1[0], corner2[0] = corner2[0], corner1[0]

        if (corner2[1] < corner1[1]):
            corner1[1], corner2[1] = corner2[1], corner1[1]

        self.corner1 = corner1
        self.corner2 = corner2



    def get_c1(self):
        return self.corner1

    def get_c2(self):
        return self.corner2

    def valid_point(self, point):
        return point[0] <= self.corner2[0] and point[0] >= self.corner1[0] and point[1] <= self.corner2[1] and point[1] >= self.corner1[1]