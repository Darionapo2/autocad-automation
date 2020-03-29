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

class SpotsBlock:

    bottom_left_point: APoint

    def __init__(self, width, height, spots_number, double = False, border = 0, outline = False):
        self.width = width
        self.height = height
        self.spots_number = spots_number
        self.double = double
        self.border = border
        self.outline = outline

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

    def add_transponders(self):
        for n in range(self.spots_number):
            x = self.bottom_left_point.x + (self.width / 2) + ((self.width + self.border) * n)
            y = self.bottom_left_point.y + 50

            transponder_insert_point = APoint(x, y)
            Transponder().draw(transponder_insert_point)

class TranspondersBlock:
    pass # TODO: Sfruttare il sistema di inserimento transponders precedentemente adottato per creare gruppi modulari di Transponders

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
    spots_block1 = SpotsBlock(140, 800, 20, double = True, border = 10, outline = True)
    spots_block1.draw(insert_point1)

    insert_point2 = APoint(0, 2000)
    spots_block2 = SpotsBlock(140, 800, 20, double = False, border = 10, outline = True)
    spots_block2.draw(insert_point2)

    insert_point3 = APoint(0, 4000)
    spots_block3 = SpotsBlock(140, 800, 20, double = True, outline = False)
    spots_block3.draw(insert_point3)

    spots_block1.add_transponders()
    spots_block2.add_transponders()
    spots_block3.add_transponders()

if __name__ == '__main__':
    main()
