import ezdxf
from ezdxf import *
from Point import *
import math

doc = ezdxf.readfile('dxf_test_files/florim_usa_research_and_development.dxf')
msp = doc.modelspace()

def distance(first_point: Point, second_point: Point) -> float:
    return math.sqrt((first_point.x - second_point.x) ** 2 + (first_point.y - second_point.y) ** 2)
