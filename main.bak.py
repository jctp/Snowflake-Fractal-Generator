#!/usr/bin/env python3

# Icon attributions
# https://www.flaticon.com/free-icon/turtle_667212?term=turtle&page=1&position=40
# https://www.flaticon.com/free-icon/snow_803477?term=snowflake&page=1&position=24

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import Image
import threading
import time

def fractalGeneration(width, height, zoom, moveX, moveY, cX, cY, maxIter):
    output = Image.new("RGB", (width, height), "white")
    pix = output.load()

    print("Starting Julia fractal generation...")


    for x in range(width):
        #print("Column: " + str(x))
        for y in range(height):
            #if y % 100 == 0 and y != width:
                #print("Row: " + str(y))
            zx = 1.5 * (x - width / 2) / (0.5 * zoom * width) + moveX
            zy = 1.0 * (y - height / 2) / (0.5 * zoom * height) + moveY
            i = maxIter
            while zx * zx + zy * zy < 4 and i > 1:
                tmp = zx * zx - zy * zy + cX
                zy, zx = 2.0 * zx * zy + cY, tmp
                i -= 1

            pix[x,y] = (i << 21) + (i << 10) + i * 8

    output.save("fractal.png", "PNG")

    headerBar.set_subtitle("Ready")
    while Gtk.events_pending():
        Gtk.main_iteration()

    mainViewport.set_from_file("fractal.png")

class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def executeButtonPressed(self, button):
        headerBar.set_subtitle("Processing...")
        while Gtk.events_pending():
            Gtk.main_iteration()
        processThread = threading.Thread(target = fractalGeneration(
        int(widthSpinner.get_text()),
        int(heightSpinner.get_text()),
        float(zoomValueSpinner.get_text()),
        float(xValue.get_text()),
        float(yValue.get_text()),
        float(cXSpinner.get_text()),
        float(cYSpinner.get_text()),
        int(iterationSpinner.get_text()),
        ))
        processThread.daemon = True
        processThread.start()

builder = Gtk.Builder()
builder.add_from_file("FractalGenerator.glade")
builder.connect_signals(Handler())

mainViewport = builder.get_object("mainOutput")
widthSpinner = builder.get_object("widthValue")
heightSpinner = builder.get_object("heightValue")
zoomValueSpinner = builder.get_object("zoomValue")
xValue = builder.get_object("xValue")
yValue = builder.get_object("yValue")
cXSpinner = builder.get_object("cX")
cYSpinner = builder.get_object("cY")
iterationSpinner = builder.get_object("iterationValue")
headerBar = builder.get_object("headerBar")

mainViewport.set_from_file("logo.png")

window = builder.get_object("mainWindow")
window.show_all()
Gtk.main()
