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
    def __init__(self, width, height, spots_number, double = False, border = 0, outline = False):
        self.width = width
        self.height = height
        self.spots_number = spots_number
        self.double = double
        self.border = border
        self.outline = outline

    def draw(self, insert_point):
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
        pass


def main():
    insert_point = APoint(200, 10000)
    spots_block = SpotsBlock(140, 800, 100, double = True)
    spots_block.draw(insert_point)

if __name__ == '__main__':
    main()
