from pyautocad import Autocad, APoint
a_cad = Autocad(create_if_not_exists = True)

def generate_rectangle(insert_point, width, height):
    a_cad.model.AddLine(insert_point, APoint(insert_point.x + width, insert_point.y))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y), APoint(insert_point.x + width, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y + height), APoint(insert_point.x, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x, insert_point.y + height), insert_point)

def generate_spot(insert_point, width, height):
    a_cad.model.AddLine(insert_point, APoint(insert_point.x + width, insert_point.y))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y + height), APoint(insert_point.x, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x, insert_point.y + height), insert_point)

def generate_single_spots_block(insert_point, width, height, spots_number, border = 0):
    for n in range(spots_number):
        if n == spots_number - 1 or border != 0:
            generate_rectangle(APoint(insert_point.x + ((width + border) * n), insert_point.y), width, height)
        else:
            generate_spot(APoint(insert_point.x + ((width + border) * n), insert_point.y), width, height)

spots_block_generated = []

def save_spots_blocks(spots_block_generated):
    pass # TODO: track all the spots blocks generated and save them into a csv file.

class SpotsBlock:

    bottom_left_point: APoint

    def __init__(self, width, height, spots_number, double = False, border = 0, outline = False):
        self.width = width
        self.height = height
        self.spots_number = spots_number
        self.double = double
        self.border = border
        self.outline = outline

        # TODO: register into the save_spots_blocks all the instances of this class.

    def draw(self, insert_point):

        self.bottom_left_point = insert_point

        for n in range(self.spots_number):
            if n == self.spots_number - 1 or self.border != 0:
                generate_rectangle(APoint(insert_point.x + ((self.width + self.border) * n), insert_point.y), self.width, self.height)
            else:
                generate_spot(APoint(insert_point.x + ((self.width + self.border) * n), insert_point.y), self.width, self.height)

        if self.double:
            upper_spots_block_insert_point = APoint(insert_point.x, insert_point.y + self.height + self.border)

            generate_single_spots_block(upper_spots_block_insert_point, self.width, self.height, self.spots_number, self.border)

        if self.outline:
            rectangle_insert_point = APoint(insert_point.x - self.border, insert_point.y - self.border)
            rectangle_width = (self.width + self.border) * self.spots_number + self.border
            rectangle_height = self.height + (2 * self.border) if not self.double else (2 * self.height) + (3 * self.border)

            generate_rectangle(rectangle_insert_point, rectangle_width, rectangle_height)

    def add_transponders(self, internal_distance_from_spots_border = 50, external_distance_from_spots_border = 140, mode = 'bottom'):

        x = self.bottom_left_point.x + (self.width / 2)
        layers_number = 2 if self.double else 1

        def bottom_mode():
            y = self.bottom_left_point.y + \
                internal_distance_from_spots_border

            TranspondersBlock(self.spots_number, self.width + self.border).draw(APoint(x, y))

            y = self.bottom_left_point.y - \
                external_distance_from_spots_border

            TranspondersBlock(self.spots_number, self.width + self.border).draw(APoint(x, y))

        def top_mode():
            offset_factor = (layers_number * self.height) + \
                            self.border

            y = self.bottom_left_point.y + \
                offset_factor - \
                internal_distance_from_spots_border

            TranspondersBlock(self.spots_number, self.width + self.border).draw(APoint(x, y))

            y = self.bottom_left_point.y + \
                offset_factor + \
                external_distance_from_spots_border

            TranspondersBlock(self.spots_number, self.width + self.border).draw(APoint(x, y))

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

class TranspondersBlock:

    first_transponder_center_point: APoint

    def __init__(self, transponders_number, distance):
        self.transponders_number = transponders_number
        self.distance = distance

    def draw(self, insert_point):

        self.first_transponder_center_point = insert_point

        for n in range(self.transponders_number):
            x = self.first_transponder_center_point.x + (self.distance * n)
            y = self.first_transponder_center_point.y

            transponder_insert_point = APoint(x, y)
            Transponder().draw(transponder_insert_point)

class Transponder:
    def __init__(self, scale_factor = 36):
        self.scale_factor = scale_factor

    def draw(self, insert_point):
        half_scale_factor = self.scale_factor / 2
        quarter_scale_factor = half_scale_factor / 2

        left_point = APoint(insert_point.x - half_scale_factor, insert_point.y)
        right_point = APoint(insert_point.x + half_scale_factor, insert_point.y)
        top_point = APoint(insert_point.x, insert_point.y + half_scale_factor)
        bottom_point = APoint(insert_point.x, insert_point.y - half_scale_factor)

        left_side_point = APoint(insert_point.x - (self.scale_factor / 9), insert_point.y - quarter_scale_factor)
        right_side_point = APoint(insert_point.x + (self.scale_factor / 9), insert_point.y - quarter_scale_factor)

        a_cad.model.AddLine(left_point, right_point)
        a_cad.model.AddLine(top_point, bottom_point)
        a_cad.model.AddLine(left_side_point, right_side_point)

def main():
    insert_point1 = APoint(0, 0)
    spots_block1 = SpotsBlock(140, 900, 100, double = True, border = 10, outline = True)
    spots_block1.draw(insert_point1)

    spots_block1.add_transponders(mode = 'both')

if __name__ == '__main__':
    main()
