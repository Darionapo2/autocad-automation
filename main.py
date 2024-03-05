import ezdxf
import pprint

import matplotlib.pyplot as plt

import Point
from Number import *
from SpotsBlock import *
from Global import doc
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

'''
# METODO RISOLUTIVO 2
# calcolo i coefficienti angolari
m1 = round((y12 - y11) / (x12 - x11), 6)
m2 = round((y22 - y21) / (x22 - x21), 6)

# print('m1:', m1, 'm2:', m2)

if m1 == m2:
    print('M1 == M2 TRUEEEE')
    return True
'''

def m(line): # line: ((x1, y1), (x2, y2))
    x1 = line[0][0]
    y1 = line[0][1]

    x2 = line[1][0]
    y2 = line[1][1]

    return (y2 - y1) / (x2 - x1)

class Main:

    @staticmethod
    def tests() -> dict:

        """
        setup = {
            'width' : 140,
            'height' : 800,
            'spots_number' : 30,
            'double' : True,
            'border' : 10,
            'outline' : True
        }

        setup2 = {
            'width' : 150,
            'height' : 400,
            'spots_number' : 10,
            'double' : True,
            'border' : 5,
            'outline' : False
        }

        insert_point2 = Point(0, 10000)
        spots_block2 = SpotsBlock.from_dict(setup = setup)
        spots_block2.draw(insert_point2)
        insert_point3 = Point(0, 20000)
        spots_block3 = SpotsBlock(140, 400, 11, double = False, border = 10, outline = True)
        spots_block3.draw(insert_point3)

        insert_point4 = Point(0, 30000)
        spots_block4 = SpotsBlock(140, 900, 20, double = True, border = 0, outline = False)
        spots_block4.draw(insert_point4)

        insert_point5 = Point(0, 40000)
        spots_block5 = SpotsBlock(140, 900, 20, double = False, border = 0, outline = True)
        spots_block5.draw(insert_point5)

        #spots_block2.add_transponders()
        spots_block3.add_transponders()

        #spots_block2.enumerate()
        spots_block3.enumerate()
        spots_block4.enumerate()
        spots_block5.enumerate()

        blocks_block_setup_model = {
            'vertical_blocks_distance': 450,
            'horizontal_blocks_distance': 450,

            'mode': 0,
            'mode_zero': {
                'vertical_blocks_number': 5,
                'horizontal_blocks_number': 10
            },

            'mode_one': {
                'total_width': 2000,
                'total_height': 10000
            }
        }

        blocks_block_setup_model2 = {
            'vertical_blocks_distance': 450,
            'horizontal_blocks_distance': 450,

            'mode': 1,
            'mode_zero': {
                'vertical_blocks_number': 5,
                'horizontal_blocks_number': 3
            },

            'mode_one': {
                'total_width': 30000,
                'total_height': 10000
            }
        }

        insert_point6 = Point(30000, 50000)
        insert_point7 = Point(30000, 10000)

        BlocksBlock(setup, blocks_block_setup_model).draw(insert_point6)
        BlocksBlock(setup2, blocks_block_setup_model2).draw(insert_point7)

        """
        """
        r1 = Rectangle()
        r1.generate_rectangle(Point(0, 0), 30, 30)

        r2 = Rectangle()
        r2.generate_rectangle(Point(100, 0), 30, 30)

        entities_list = DocumentReader.get_all_entities()
        for entity in entities_list:
            print(entity.dxf.layer)

        column_bottom_left_point_location1 = entities_list[0].vertices[0].dxf.location
        column_bottom_left_point_location2 = entities_list[1].vertices[0].dxf.location


        column_bottom_left_point1 = Point(column_bottom_left_point_location1[0], column_bottom_left_point_location1[1])
        column_bottom_left_point2 = Point(column_bottom_left_point_location2[0], column_bottom_left_point_location2[1])

        doc.save()
        """

        # CODICE PER CONTARE I PUNTI SU UN DATO LAYER E OTTENERE LE COORDINATE SU UN FILE DI OUTPUT
        all_entities = DocumentReader.get_all_entities()
        polylines = []
        output_log = 'Idrotherm_nuova_tracciatura_19_02_24.csv'
        with (open(output_log, mode = 'w+', encoding = 'utf-8') as outfile):

            for e in all_entities:
                if (e.dxf.layer == 'aree_gps_nuova_tracciatura' or
                    e.dxf.layer == 'WF ingombro stive 2' or
                    e.dxf.layer == 'WF piazzole' or
                    e.dxf.layer == 'aree gps 3'):


                    vertices = list(e.vertices())
                    rounded_vertices = [(math.trunc(x), math.trunc(y)) for x, y in vertices]
                    if (rounded_vertices[-1][0] - 100 < rounded_vertices[0][0] < rounded_vertices[-1][0] + 100) and (rounded_vertices[-1][1] - 100 < rounded_vertices[0][1] < rounded_vertices[-1][1] + 100):
                        del rounded_vertices[-1]
                    polylines.append(rounded_vertices)

            # ordina i vertici delle aree gps in ordine crescente per la coordinata x
            # polylines = [sorted(polyline, key = lambda x: x[0]) for polyline in polylines]

            # ordina le liste di vertici delle aree gps partendo dal primo in ordine crescente per x
            polylines = sorted(polylines, key = lambda x: x[0])

            # PLOTTING
            # Plot each polyline
            for polyline in polylines:
                # Extract x and y coordinates
                x, y = zip(*polyline)

                # Close the polyline by connecting the last point to the first point
                x = list(x) + [x[0]]
                y = list(y) + [y[0]]

                # Plot the polyline
                plt.plot(x, y, color = 'g')

            plt.axis('equal')
            plt.tight_layout()
            plt.axis('off')

            # print('polylines: ' + str(polylines))
            print('numero polylines:', len(polylines))

            # estrae i vari testi e la relativa posizione dal DWG
            texts = {}
            for e2 in all_entities:
                if e2.dxf.layer == 'WF nome aree GPS':
                    text = e2.dxf.text
                    text_pos = list(e2.get_placement()[1])[:2]
                    rounded_text_pos = [math.trunc(coord) for coord in text_pos]
                    rounded_text_pos = tuple(rounded_text_pos)
                    texts.update({text: rounded_text_pos})

                    #PLOTTING
                    plt.text(text_pos[0], text_pos[1], text, fontsize = 5, color = 'black')
            print('numero texts: ', len(texts))

            # estrae le entry lines
            entry_lines = []
            for e3 in all_entities:
                if e3.dxf.layer == 'WF_lato_di_accesso_2' or e3.dxf.layer == 'WF lato di accesso':
                    start = list(e3.dxf.start)[:2]
                    end = list(e3.dxf.end)[:2]
                    start = [math.trunc(coord) for coord in start]
                    end = [math.trunc(coord) for coord in end]
                    entry_line = (tuple(start), tuple(end))
                    entry_lines.append(entry_line)

                    # PLOTTING
                    x, y = zip(*entry_line)
                    plt.plot(x, y, color = 'r', linewidth = 2)
                    plt.plot(x[0], y[0], marker = '*', markersize = 7, color = 'm')
            '''
            left_points = []
            for e4 in all_entities:
                if e4.dxf.layer == 'WF vertice sinistro':
                    x = math.trunc(e4.dxf.location[0])
                    y = math.trunc(e4.dxf.location[1])
                    left_points.append((x, y))
            '''

            # print('entry lines:')
            # pprint.pprint(entry_lines)
            print('numero entry lines: ', len(entry_lines))


            '''
            print('left points: ', left_points)
            print(len(left_points))
            if len(left_points) != len(entry_lines):
                print('MANCA QUALCHE PUNTO O QUALCHE ENTRY LINE')
            '''

            plt.show()

            gps_areas = {}
            for txt, pos in texts.items():
                # print('\n\nentry line:', el)
                # entry_side = None
                for polyline in polylines:
                    if test_point(pos[0], pos[1], polyline):
                        gps_areas.update({txt: []})
                        gps_areas[txt].append(polyline)

                        for el in entry_lines:
                            el_rounded = tuple([(math.trunc(x/100), math.trunc(y/100)) for x, y in el])
                            polyline_rounded = tuple([(math.trunc(x/100), math.trunc(y/100)) for x, y in polyline])
                            if set(el_rounded).issubset(set(polyline_rounded)):
                                gps_areas[txt].append(el)
                                '''
                                for left_point in left_points:
                                    if left_point in el:
                                        gps_areas[txt].append(left_point)
                                # print('TROVATO')
                                '''

                        '''
                        shifted_polyline = polyline.copy()
                        shifted_polyline.append(shifted_polyline[0])
                        shifted_polyline = shifted_polyline[1:]
                        # print('\tshifted polyline:', shifted_polyline)
                        for first, second in zip(polyline, shifted_polyline):
                            # print('\t\tfirst:', first, 'second:', second)
                            if overlaps(el, (first, second), 100):
                                entry_side = (first, second)
                                print('\tTROVATO!!')
                                print('\tentry side:', entry_side)
                                print('\tpolyline:', polyline)
                                # print('entry line:', el)
                                print('\n\n')

                                gps_areas[txt].append(entry_side)
                                break
                        if entry_side is not None:
                            break
                        '''

            sorted_gps_areas = {key: value for key, value in sorted(gps_areas.items())}
            for gps_area_name, info in sorted_gps_areas.items():
                if len(info) < 1:
                    print('ERRORE MANCA UNA ENTRY LINE IN:', gps_area_name)
            # pprint.pprint(gps_areas)
            # print(len(gps_areas))
            # print(texts)
            # print(is_coincident_rounded(((24324, 5325), (23124, 4556)), ((24324, 5325), (23124, 4556)), 100))


            for area_name, info in sorted_gps_areas.items():
                # print(info)
                outfile.write('\narea: \"' + area_name + '\"' + ',')
                for coords in info[0]:
                    outfile.write(str(coords[0]) + ',' + str(coords[1]) + ',')
                if len(info) > 1:
                    for coords in info[1]:
                        outfile.write(str(coords[0]) + ',' + str(coords[1]) + ',')
                if len(info) > 2:
                    for coords in info[2]:
                        outfile.write(str(coords) + ',')
                if len(info) > 3:
                    for coords in info[3]:
                        outfile.write(str(coords) + ',')


        return sorted_gps_areas


if __name__ == '__main__':
    Main().tests()




'''
    for el in entry_lines:
        outfile.write('\n')
        for coords in el:
            outfile.write(str(coords[0]) + ',' + str(coords[1]) + ',')
'''
'''
points = [(24037, 15219), (23693, 15662), (23507, 15907),
          (23205, 16303), (23031, 16528), (22614, 17047),
          (22199, 17588), (21843, 18053), (21589, 18353),
          (21244, 18758), (21024, 19017), (20801, 19276)]

attr = {
    'layer' : 'wfreg'
}

mm_points = [(point[0] * 10, point[1] * 10) for point in points]
for point in mm_points:
    msp.add_point(location = point, dxfattribs = attr)

msp.add_polyline2d(mm_points, dxfattribs = attr)

doc.saveas('test2.dxf')

'''
