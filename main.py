from Bounds import Bounds
from Layer import Layer

bounds = Bounds((10,10), (200,189))
layer = Layer(bounds, 3, 2080)
layer.plot_points()