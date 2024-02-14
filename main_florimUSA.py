import ezdxf
import pprint

from ezdxf.enums import TextEntityAlignment

import Point
from Number import *
from SpotsBlock import *
from Global import doc, distance
from BlockBlocks import *
from Rectangle import *
from DocumentReader import *
from Global import msp
import math

def is_on_right_side(x, y, xy0, xy1):
    x0, y0 = xy0
    x1, y1 = xy1
    a = float(y1 - y0)
    b = float(x0 - x1)
    c = - a*x0 - b*y0
    return a*x + b*y + c >= 0

def test_point(x, y, vertices):
    num_vert = len(vertices)
    is_right = [is_on_right_side(x, y, vertices[i], vertices[(i + 1) % num_vert]) for i in range(num_vert)]
    all_left = not any(is_right)
    all_right = all(is_right)
    return all_left or all_right

def overlaps(line1, line2, round_factor):
    line1 = sorted(line1, key = lambda x: x[0])
    line2 = sorted(line2, key = lambda x: x[0])
    # primo punto della linea 1
    x11 = math.trunc(line1[0][0] / round_factor)
    y11 = math.trunc(line1[0][1] / round_factor)

    # secondo punto della linea 1
    x12 = math.trunc(line1[1][0] / round_factor)
    y12 = math.trunc(line1[1][1] / round_factor)

    # primo punto della linea 2
    x21 = math.trunc(line2[0][0] / round_factor)
    y21 = math.trunc(line2[0][1] / round_factor)

    # secondo punto della linea 2
    x22 = math.trunc(line2[1][0] / round_factor)
    y22 = math.trunc(line2[1][1] / round_factor)

    if x11 != x21 or y11 != y21 or x12 != x22 or y12 != y22:
        # print('linee:', line1, line2)
        return False

    return True

def m(line): # line: ((x1, y1), (x2, y2))
    x1 = line[0][0]
    y1 = line[0][1]

    x2 = line[1][0]
    y2 = line[1][1]

    return (y2 - y1) / (x2 - x1)


def lowest_coordinates_vertex(vs):
    return min(vs, key = lambda v: (v[1], v[0]), default = None)


def florim_usa_test():
    all_entities = DocumentReader.get_all_entities()

    wf_numbers = []
    rows = []
    for entry in all_entities:
        if entry.dxf.layer == 'WF_all_bays':
            if type(entry) == ezdxf.entities.insert.Insert:
                # print(list(entry.dxf.insert)[:2], '-->', entry.dxf.name)
                rows.append(entry)

        if entry.dxf.layer == 'WF_numbers':
            if entry.dxf.text.isnumeric():
                wf_numbers.append(entry)

    rows_closest_num = {}
    for row in rows:
        row_name = row.dxf.name
        searched_row_names = ['WF 125x231in bay', 'WF 10x18ft bay', 'WF 10x36ft bay', 'WF 10x9ft bay', 'WF 120x224in bay', 'WF staging bay', 'WF 10x34ft bay', 'WF 10x15ft bay', 'WF 10x16ft bay']
        row_location = Point(math.trunc(row.dxf.insert[0]), math.trunc(row.dxf.insert[1]))
        str_row_location = 'x: ' + str(math.trunc(row.dxf.insert[0])) + ' y: ' + str(math.trunc(row.dxf.insert[1]))

        if row_name in searched_row_names:

            # IDENTIFY OF THE BLOCK DEFINITION
            row_block_def = doc.blocks[row_name]

            # SEARCH FOR THE CLOSEST ROW NUMBER
            record_distance = 1000_000_000
            record_n = wf_numbers[0]

            for n in wf_numbers:
                n_location = Point(n.dxf.insert[0], n.dxf.insert[1])
                dist = distance(n_location, row_location)

                if dist < record_distance:
                    record_distance = dist
                    record_n = n

            # TRANSLATION OF ALL THE ROWS RECTANGLES TO GET THE ABSOLUTE COORDINATES IN THE WHOLE DRAWING
            rectangle = row_block_def.query('LWPOLYLINE')
            rectangle = list(rectangle[0].vertices())
            lowest_x, lowest_y = lowest_coordinates_vertex(rectangle)
            translated_rectangle = [(x - lowest_x, y - lowest_y) for x, y in rectangle]

            # print('rectangle:', rectangle)
            # print('lowest vertex:', lowest_x, lowest_y)
            # print('translated rect:', translated_rectangle)

            # ACTUAL COORDINATES CALCULATION USING THE BLOCK INSERTION POINT --> IS IMPLIED THAT THE INSERTION POINT IS THE BOTTOM LEFT VERTEX OF THE ROW
            if row.dxf.rotation == 0:
                placed_rect = [(x + row.dxf.insert[0], y + row.dxf.insert[1]) for x, y in translated_rectangle]
            elif 179 < row.dxf.rotation < 181:
                placed_rect = [(-x + row.dxf.insert[0], -y + row.dxf.insert[1]) for x, y in translated_rectangle]
            else:
                print('error: rotation degree not valid.', row.dxf.rotation)
                placed_rect = None

            # print('placed rectangle:', placed_rect)

            rounded_placed_rect = [(int(round(x, 0)), int(round(y))) for x, y in placed_rect]

            relative_row_number = record_n.dxf.text
            rows_closest_num.update({row_name + '__' + relative_row_number + '__' + str_row_location: [record_distance, record_n.dxf.insert, [int(round(row.dxf.insert[0], 0)), int(round(row.dxf.insert[1], 0))], rounded_placed_rect, int(relative_row_number)]})

            # UPDATE OF THE DXF FILE WHERE I ADD SOME TEXT TO NAME EACH ROW UNIQUELY
            displacement_y = +2000 if row.dxf.rotation == 0 else -2000
            displacement_x = 0 if row.dxf.rotation == 0 else -2500

            msp.add_mtext(text = f'{row_name}\P{str_row_location}',
                         dxfattribs = {
                            'insert': (row.dxf.insert[0] + displacement_x, row.dxf.insert[1] + displacement_y),
                            'char_height': 200
                         })

    # SIMPLE PRINT OF ALL ROWS SAVED INTO THE DICTIONARY
    i = 0
    for key, value in rows_closest_num.items():
        i += 1
        print(i, key, value)

    doc.saveas('FLORIM_TEST.dxf')

    with open('out15.csv', 'w+', encoding = 'utf-8') as outfile:
        outfile.write('row name,row number,x insert point,y insert point,x1,y1,x2,y2,x3,y3,x4,y4')

        for name, objs in rows_closest_num.items():
            outfile.write(f'\n{name.split("__")[0]},')
            outfile.write(f'{objs[4]},')
            outfile.write(f'{objs[2][0]},{objs[2][1]},')
            for rect_coords in objs[3]:
                outfile.write(f'{rect_coords[0]},{rect_coords[1]},')

if __name__ == '__main__':
    florim_usa_test()