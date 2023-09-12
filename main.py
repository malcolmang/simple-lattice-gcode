from Bounds import Bounds
from Print import Print

bounds = Bounds((0,0), (6,6))
printobj = Print(bounds, 1, 45, 6, 0.3, 420)
printobj.generate_gcode(print = True)
