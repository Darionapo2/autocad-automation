import Point
from Number import *
from SpotsBlock import *
from Global import doc
from BlockBlocks import *

class Main:

    @staticmethod
    def tests() -> None:

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

        #insert_point2 = Point(0, 10000)
        #spots_block2 = SpotsBlock.from_dict(setup = setup)
        #spots_block2.draw(insert_point2)
        '''
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
        '''

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

        it = doc.entities.__iter__()

        for obj in it:
            print(obj)

        doc.save()

if __name__ == '__main__':
    Main().tests()
