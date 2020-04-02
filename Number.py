from Point import *
from Global import msp

class Number:
    def __init__(self, value: int, scale_factor: float = 1):
        self.value = value
        self.scale_factor = scale_factor

    def draw(self, insert_point: Point):
        style = {
            'layer' : 'NUMBERS',
            'style' : '1',
            'text_generation_flag' : 1,
            'height' : 120 * self.scale_factor,
            'color' : 6
        }

        p = (insert_point.x, insert_point.y)
        msp.add_text(str(self.value), dxfattribs = style).set_pos(p, align = 'CENTER')
