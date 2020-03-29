from pyautocad import Autocad, APoint
a_cad = Autocad(create_if_not_exists = True)

def main():
    insert_point = APoint(200, 1000)
    generate_spots(insert_point, 140, 500, 87, double = True, border = 10)

def generate_rectangle(insert_point, width, height):
    a_cad.model.AddLine(insert_point, APoint(insert_point.x + width, insert_point.y))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y), APoint(insert_point.x + width, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y + height), APoint(insert_point.x, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x, insert_point.y + height), insert_point)

def generate_spot(insert_point, width, height):
    a_cad.model.AddLine(insert_point, APoint(insert_point.x + width, insert_point.y))
    a_cad.model.AddLine(APoint(insert_point.x + width, insert_point.y + height), APoint(insert_point.x, insert_point.y + height))
    a_cad.model.AddLine(APoint(insert_point.x, insert_point.y + height), insert_point)

def generate_spots(insert_point, width, height, number, double = False, border = 0):
    for n in range(number):
        if n == number - 1:
            generate_rectangle(APoint(insert_point.x + ((width + border) * n), insert_point.y), width, height)
        else:
            generate_spot(APoint(insert_point.x + ((width + border) * n) + border, insert_point.y), width, height)

    if double:
        generate_spots(APoint(insert_point.x, insert_point.y + height + border), width, height, number)

if __name__ == '__main__':
    main()
