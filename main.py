import Point
from Number import *
from SpotsBlock import *
from Global import doc

class Main:

    @staticmethod
    def tests() -> None:

        insert_point2 = Point(0, 10000)
        spots_block2 = SpotsBlock(150, 500, 55, double = True, border = 15, outline = True)
        spots_block2.draw(insert_point2)

        insert_point3 = Point(0, 20000)
        spots_block3 = SpotsBlock(140, 400, 11, double = False, border = 10, outline = True)
        spots_block3.draw(insert_point3)

        insert_point4 = Point(0, 30000)
        spots_block4 = SpotsBlock(140, 900, 20, double = True, border = 0, outline = False)
        spots_block4.draw(insert_point4)

        insert_point5 = Point(0, 40000)
        spots_block5 = SpotsBlock(140, 900, 20, double = False, border = 0, outline=True)
        spots_block5.draw(insert_point5)

        spots_block2.add_transponders()
        spots_block3.add_transponders()
        spots_block4.add_transponders()
        spots_block5.add_transponders()

        insert_point6 = Point(0, 0)
        Number(1).draw(insert_point6)

        doc.save()

if __name__ == '__main__':
    Main().tests()
