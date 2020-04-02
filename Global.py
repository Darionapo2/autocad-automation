import ezdxf

doc = ezdxf.readfile('dxf_test_files/tests.dxf')
msp = doc.modelspace()