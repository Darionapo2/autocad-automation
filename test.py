import ezdxf


if __name__ == '__main__':
    doc = ezdxf.readfile('dxf_test_files/test.dxf')
    msp = doc.modelspace()

    msp.add_text(text = 'hello world',
                 dxfattribs = {
                     'insert': (0, 0),
                     'height': 10
                 })

    doc.saveas('test_saved.dxf')
