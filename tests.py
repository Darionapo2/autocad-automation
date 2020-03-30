# Import needed modules
import os
import comtypes.client
from comtypes import COMError
from comtypes.client import CreateObject, GetActiveObject


def main():
    try:  # Get AutoCAD running instance
        acad = GetActiveObject("AutoCAD.Application.20")
        state = True
    except(OSError, COMError):  # If autocad isn't running, open it
        acad = CreateObject("AutoCAD.Application.20", dynamic=True)
        state = False

    if state:  # If you have only 1 opened drawing
        doc = acad.Documents.Items(0)
    else:
        filepath = "E:/Dir1/Dir2/myDWG.dwg"  # Replace it with the actual drawing path
        doc = acad.Documents.Open(filepath)

    # Our example command is to draw a line from (0,0) to (5,5)
    command_str = '._line '  # Notice that the last SPACE is equivalent to hiting ENTER
    # You should separate the command's arguments also with SPACE

    # Send the command to the drawing
    doc.SendCommand(command_str)


# Execution Part
if __name__ == '__main__':
    main()