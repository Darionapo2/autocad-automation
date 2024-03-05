import ezdxf
from ezdxf import *
from Point import *
import math

doc = ezdxf.readfile('dxf_test_files/Idrotherm 2000 disposizione aree GPS v11 25-02-2024.dxf')
msp = doc.modelspace()

def distance(first_point: Point, second_point: Point) -> float:
    return math.sqrt((first_point.x - second_point.x) ** 2 + (first_point.y - second_point.y) ** 2)
