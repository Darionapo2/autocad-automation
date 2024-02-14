import ezdxf
import numpy
from main import Main

doc = ezdxf.readfile('redo/test1.dxf')
msp = doc.modelspace()



if __name__ == "__main__":
    m = Main()
    d = m.tests()

    print(d)

    for e in msp:
        print(e)
        e.destroy()

    for area, data in d.items():
        points = data[0]
        msp.add_lwpolyline(points, close = True, dxfattribs = {'layer' : 'aree GPS'})

        el_points = data[1]
        msp.add_line(el_points[0], el_points[1], dxfattribs = {'layer' : 'lati di accesso'})


    doc.saveas("redo/test1.dxf")


