from pyautocad import Autocad, APoint
a_cad = Autocad(create_if_not_exists = True)

def main():
    insert_point = APoint(200, 5000)
    generate_spots_block(insert_point, 140, 500, 87, double = True, border = 10, outline = True)

def generate_rectangle(insert_point, width, height):
    a_cad.model.AddLine(insert_point, APoint(insert_point.x + width, insert_point.y))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y), APoint(insert_point.x + width, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y + height), APoint(insert_point.x, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x, insert_point.y + height), insert_point)

def generate_spot(insert_point, width, height):
    a_cad.model.AddLine(insert_point, APoint(insert_point.x + width, insert_point.y))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y + height), APoint(insert_point.x, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x, insert_point.y + height), insert_point)

def generate_spots_block(insert_point, width, height, number, double = False, border = 0, outline = False):
    for n in range(number):
        if n == number - 1 or border != 0:
            generate_rectangle(APoint(insert_point.x + ((width + border) * n), insert_point.y), width, height)
        else:
            generate_spot(APoint(insert_point.x + ((width + border) * n), insert_point.y), width, height)

    if double:
        generate_spots_block(APoint(insert_point.x, insert_point.y + height + border), width, height, number, border = border)

    if outline:
        rectangle_insert_point = APoint(insert_point.x - border, insert_point.y - border)
        rectangle_width = (width + border) * number + border
        rectangle_height = height + (2 * border) if not double else (2 * height) + (3 * border)

        generate_rectangle(rectangle_insert_point, rectangle_width, rectangle_height)

def add_transponder():
    pass

if __name__ == '__main__':
    main()
