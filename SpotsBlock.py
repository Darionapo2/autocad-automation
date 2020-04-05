from TranspondersBlock import *
from Number import *
from Rectangle import *

class SpotsBlock:

    bottom_left_point: Point
    first_spot_bottom_center: Point

    def __init__(self,
                 width: float,
                 height: float,
                 spots_number: int,
                 double: bool = False,
                 border: float = 0,
                 outline: bool = False):

        self.width = width
        self.height = height
        self.spots_number = spots_number
        self.double = double
        self.border = border
        self.outline = outline

        self.layers_number = 2 if self.double else 1

        self.offset_factor = (self.layers_number * self.height) + self.border

    @classmethod
    def from_dict(cls, setup: dict):
        return cls(width = setup['width'],
                   height = setup['height'],
                   spots_number = setup['spots_number'],
                   double = setup['double'],
                   border = setup['border'],
                   outline = setup['outline'])

    def generate_single_spots_block(self, insert_point: Point) -> None:

        for n in range(self.spots_number):
            p = Point(insert_point.x + ((self.width + self.border) * n), insert_point.y)
            Rectangle().generate_rectangle(p, self.width, self.height)

    def draw(self, insert_point: Point) -> None:

        self.bottom_left_point = insert_point
        self.first_spot_bottom_center = Point(self.bottom_left_point.x + (self.width / 2), self.bottom_left_point.y)

        for n in range(self.spots_number):
            p1 = Point(insert_point.x + ((self.width + self.border) * n), insert_point.y)
            Rectangle().generate_rectangle(p1, self.width, self.height)

        if self.double:
            upper_spots_block_insert_point = Point(insert_point.x, insert_point.y + self.height + self.border)
            self.generate_single_spots_block(upper_spots_block_insert_point)

        if self.outline:
            rectangle_insert_point = Point(insert_point.x - self.border, insert_point.y - self.border)
            rectangle_width = (self.width + self.border) * self.spots_number + self.border
            rectangle_height = self.height + (2 * self.border) \
                if not self.double else (2 * self.height) + (3 * self.border)

            Rectangle().generate_rectangle(rectangle_insert_point, rectangle_width, rectangle_height)

    def add_transponders(self,
                         internal_distance_from_borders: float = 50,
                         external_distance_from_borders: float = 140,
                         mode: str = 'bottom') -> None:

        x = self.first_spot_bottom_center.x

        def bottom_mode():
            y = self.bottom_left_point.y + \
                internal_distance_from_borders

            TranspondersBlock(self.spots_number, self.width + self.border).draw(Point(x, y))

            y = self.bottom_left_point.y - \
                external_distance_from_borders

            TranspondersBlock(self.spots_number, self.width + self.border).draw(Point(x, y))

        def top_mode():

            y = self.bottom_left_point.y + \
                self.offset_factor - \
                internal_distance_from_borders

            TranspondersBlock(self.spots_number, self.width + self.border).draw(Point(x, y))

            y = self.bottom_left_point.y + \
                self.offset_factor + \
                external_distance_from_borders

            TranspondersBlock(self.spots_number, self.width + self.border).draw(Point(x, y))

        if mode == 'bottom':
            bottom_mode()
        elif mode == 'top':
            top_mode()
        elif mode == 'both':
            bottom_mode()
            top_mode()
        else:
            # The mode value is invalid
            # TODO: handle this error.
            pass

    def enumerate(self):

        y1 = self.bottom_left_point.y - 150 # for bottom numeration
        y2 = self.first_spot_bottom_center.y + self.offset_factor + 150 # for top numeration

        x1 = self.first_spot_bottom_center.x - 25
        x2 = self.first_spot_bottom_center.x - 25 + ((self.width + self.border) * (self.spots_number - 1))

        first_bottom_number_insert_point = Point(x1, y1)
        last_bottom_number_insert_point = Point(x2, y1)

        first_top_number_insert_point = Point(x1, y2)
        last_top_number_insert_point = Point(x2, y2)

        n1 = Number(value = 1)
        n2 = Number(value = self.spots_number)

        n3 = Number(value = n1.value, rotate = True)
        n4 = Number(value=n2.value, rotate=True)

        n1.draw(first_bottom_number_insert_point)
        n2.draw(last_bottom_number_insert_point)

        n3.draw(first_top_number_insert_point)
        n4.draw(last_top_number_insert_point)

