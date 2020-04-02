from Point import *
from Global import msp

class Transponder:

    def __init__(self, scale_factor: float = 36):
        self.scale_factor = scale_factor

    def draw(self, insert_point: Point) -> None:
        half_scale_factor = self.scale_factor / 2
        quarter_scale_factor = half_scale_factor / 2

        left_point = (insert_point.x - half_scale_factor, insert_point.y)
        right_point = (insert_point.x + half_scale_factor, insert_point.y)
        top_point = (insert_point.x, insert_point.y + half_scale_factor)
        bottom_point = (insert_point.x, insert_point.y - half_scale_factor)

        left_side_point = (insert_point.x - (self.scale_factor / 9), insert_point.y - quarter_scale_factor)
        right_side_point = (insert_point.x + (self.scale_factor / 9), insert_point.y - quarter_scale_factor)

        attributes = {
            'layer' : 'TRANSPONDERS',
            'color' : 3
        }

        msp.add_line(left_point, right_point, dxfattribs = attributes)
        msp.add_line(top_point, bottom_point, dxfattribs = attributes)
        msp.add_line(left_side_point, right_side_point, dxfattribs = attributes)