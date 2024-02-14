import ezdxf.entities
from Global import *

class Wfref:
    def __init__(self, gen_line: ezdxf.entities.Line):
        self.depth = distance(Point(gen_line.dxf.start[0], gen_line.dxf.start[1]), Point(gen_line.dxf.end[0], gen_line.dxf.end[1]))