import math
import os

import matplotlib.pyplot as plt
import imageio

from pathlib import Path
from Layer import Layer
from Layer_Variable import LayerVariableSpacing


class Print:
    def __init__(self, bounds, spacing, rotation, zheight, zspacing, feed_rate, variablespacing = False):
        # initialise list of lines
        self.spacing = spacing
        self.bounds = bounds
        self.rotation = rotation
        self.zheight = zheight
        self.feed_rate = feed_rate
        self.variablespacing = variablespacing
        self.layer_list = self.generate_layers(rotation, bounds, spacing, zheight, zspacing)
        self.savestring = self.generate_savestring()

    def generate_layers(self, rotation, bounds, spacing, zheight, zspacing):
        current_height = 0
        current_rotation = 0
        layers = []
        while (current_height <= zheight - zspacing):
            current_height += zspacing # first height should be already one space up

            if self.variablespacing:
                layers.append(LayerVariableSpacing(bounds, spacing, round(current_height, 3), current_rotation))
            else:
                layers.append(Layer(bounds, spacing, round(current_height, 3), current_rotation))
            current_rotation += rotation
        return layers

    def plot_gif(self):
        # by Dave Babbit on StackOverflow
        # Modified from https://stackoverflow.com/questions/41228209/making-gif-from-images-using-imageio-in-python
        Path("png").mkdir(parents=True, exist_ok=True)
        Path("gif").mkdir(parents=True, exist_ok=True)
        for count, layer in enumerate(self.layer_list):
            layer.plot_points()
            plt.savefig(f"png/{self.savestring}L{count:03}.png", format="png")

        images = []
        for file_name in sorted(os.listdir("png")):
            if file_name.endswith('.png'):
                file_path = os.path.join("png", file_name)
                images.append(imageio.imread(file_path))
                images.append(imageio.imread(file_path))
                os.remove(file_path)

        imageio.mimwrite(f'gif/{self.savestring}.gif', images, duration=0.25)

    def generate_savestring(self):
        spacing = self.spacing if not self.variablespacing else '_var_'
        savestring = f'D{spacing}H{self.zheight}F{self.feed_rate}R{self.rotation}'
        return savestring

    def generate_gcode(self, print = False):
        header = """M107 ; fan off
G92 E0 ; reset extruder origin
G21 ; set units to mm
G90 ; absolute coordinate space position
G92 E0 ; reset extruder origin
"""
        tail = """G92 E0
M104 S0
G27 X0
M84"""
        bufferstring = header
        extruderpos = 0
        for layer in self.layer_list:
            extruderpos, gcode = layer.generate_gcode(self.feed_rate, extruderpos)
            bufferstring += gcode

        bufferstring += tail

        if print:
            Path("gcode").mkdir(parents=True, exist_ok=True)
            with open(Path("gcode").joinpath(f"{self.savestring}.gcode"), "w") as f:
                # Writing data to a file
                f.write(bufferstring)
            return f"Wrote successfully to gcode/{self.savestring}.gcode!"
        return bufferstring

