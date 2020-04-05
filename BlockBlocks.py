from SpotsBlock import *

'''
blocks_block_setup_model = {
    'vertical_blocks_distance' : 450,
    'horizontal_blocks_distance' : 450,
    
    'mode' : 0,
    'mode_zero' : {
        'vertical_blocks_number' : 3,
        'horizontal_blocks_number' : 3
    },
    
    'mode_one' : {
        'total_width' : 2000,
        'total_height' : 2000
    }
}
'''

class BlocksBlock(SpotsBlock):
    def __init__(self, one_block_setup: dict, blocks_block_setup: dict):
        SpotsBlock.__init__(self,
                            width = one_block_setup['width'],
                            height = one_block_setup['height'],
                            spots_number = one_block_setup['spots_number'],
                            double = one_block_setup['double'],
                            border = one_block_setup['border'],
                            outline = one_block_setup['outline'])

        self.one_block_width = self.border + ((self.border + self.width) * self.spots_number) \
            if self.outline else ((self.border + self.width) * self.spots_number) - self.border

        self.one_block_height = self.offset_factor + self.border \
            if self.outline else self.offset_factor - self.border

        self.one_block_setup = one_block_setup

        self.vertical_blocks_distance = blocks_block_setup['vertical_blocks_distance']
        self.horizontal_blocks_distance = blocks_block_setup['horizontal_blocks_distance']

        if blocks_block_setup['mode'] == 0:
            self.mode = 'from_blocks_number'
            self.vertical_blocks_number = blocks_block_setup['mode_zero']['vertical_blocks_number']
            self.horizontal_blocks_number = blocks_block_setup['mode_zero']['horizontal_blocks_number']
        elif blocks_block_setup['mode'] == 1:
            self.mode = 'from_rectangle'
            self.total_width = blocks_block_setup['mode_one']['total_width']
            self.total_height = blocks_block_setup['mode_one']['total_height']

    def draw_(self, insert_point: Point, columns_number: int, rows_number: int) -> None:
        for i in range(rows_number):
            for j in range(columns_number):
                p = Point(insert_point.x + ((self.horizontal_blocks_distance + self.one_block_width) * j),
                          insert_point.y + (self.one_block_height + self.vertical_blocks_distance + self.border) * i)
                SpotsBlock.from_dict(self.one_block_setup).draw(p)

    def draw(self, insert_point: Point) -> None:
        if self.mode == 'from_blocks_number':
            self.draw_(insert_point, self.horizontal_blocks_number, self.vertical_blocks_number)
        elif self.mode == 'from_rectangle':
            columns_number = 0
            while (self.one_block_width + self.horizontal_blocks_distance) * columns_number < self.total_width:
                columns_number += 1

            rows_number = 0
            while (self.one_block_height + self.vertical_blocks_distance) * rows_number < self.total_height:
                rows_number += 1

            self.draw_(insert_point, columns_number, rows_number)

