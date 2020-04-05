from Point import *
from Global import msp

class Number:
    def __init__(self, value: int, rotate: bool = False, scale_factor: float = 1):
        self.value = value
        self.is_rotate = rotate
        self.scale_factor = scale_factor

    def draw(self, insert_point: Point):

        setup = {
            'layer' : 'NUMBERS',
            'rotation' : 180 if self.is_rotate else 0,
            # 'style' : 'LiberationSerif', TODO: someday I'll find the way to change the font, but that day isn't today.
            'width' : 0.65,
            'text_generation_flag' : 1,
            'height' : 120 * self.scale_factor,
            'color' : 6
        }

        number_insert_point = (insert_point.x, insert_point.y)
        msp.add_text(str(self.value), dxfattribs = setup).set_pos(number_insert_point, align = 'CENTER')
