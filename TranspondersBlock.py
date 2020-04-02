from Transponders import *

class TranspondersBlock(Transponder):

    first_transponder_center_point: Point

    def __init__(self, transponders_number: int, distance: float, scale_factor: float = 36):
        Transponder.__init__(self, scale_factor = scale_factor)
        self.transponders_number = transponders_number
        self.distance = distance

    def draw(self, insert_point: Point) -> None:

        self.first_transponder_center_point = insert_point

        for n in range(self.transponders_number):
            x = self.first_transponder_center_point.x + (self.distance * n)
            y = self.first_transponder_center_point.y

            transponder_insert_point = Point(x, y)
            Transponder().draw(transponder_insert_point)
