from Point import *
from Global import msp

class Rectangle:

    @staticmethod
    def generate_rectangle(insert_point: Point, width: float, height: float) -> None:
        v1 = (insert_point.x, insert_point.y)
        v2 = (insert_point.x + width, insert_point.y)
        v3 = (insert_point.x + width, insert_point.y + height)
        v4 = (insert_point.x, insert_point.y + height)

        attributes = {
            'layer' : 'COLUMNS', # TODO: change back this parameter to 'SPOTS'.
            'flags' : 1
        }

        msp.add_polyline2d([v1, v2, v3, v4, v1], dxfattribs = attributes)
