from Bounds import Bounds
from Print import Print

bounds = Bounds((0,0), (10,10))
printobj = Print(bounds, [0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5], 90, 6, 0.3, 420, variablespacing=True)
printobj.generate_gcode(print = True)
printobj.plot_gif()

printobj2 = Print(Bounds((0,0), (20,20)), 1, 10, 6, 0.3, 420)
printobj2.generate_gcode(print = True)
printobj2.plot_gif()