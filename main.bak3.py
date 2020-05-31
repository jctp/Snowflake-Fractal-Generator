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

settings = Gtk.Settings.get_default()
settings.set_property("gtk-application-prefer-dark-theme", True)

def fractalGeneration(width, height, zoom, moveX, moveY, cX, cY, maxIter):

    if supersamplingCheck.get_active() == True:
        width = width * 2
        height = height * 2
        print("Supersampling enabled")

    elif hypersamplingCheck.get_active() == True:
        width = width * 4
        height = height * 4
        print("Hypersampling enabled")

    elif ubersamplingCheck.get_active() == True:
        width = width * 8
        height = height * 8
        print("Ubersampling enabled")

    output = Image.new("RGB", (width, height), "white")
    pix = output.load()

    print("Starting Julia fractal generation...")

    for x in range(width):
        for y in range(height):

            zx = 1.5 * (x - width / 2) / (0.5 * zoom * width) + moveX
            zy = 1.0 * (y - height / 2) / (0.5 * zoom * height) + moveY
            i = maxIter
            while zx * zx + zy * zy < 4 and i > 1:
                tmp = zx * zx - zy * zy + cX
                zy, zx = 2.0 * zx * zy + cY, tmp
                i -= 1

            pix[x,y] = (i << 21) + (i << 10) + i * 8

    if supersamplingCheck.get_active() == True:
        output = output.resize((int(width / 2), int(height / 2)))

    elif hypersamplingCheck.get_active() == True:
        output = output.resize((int(width / 4), int(height / 4)))

    elif ubersamplingCheck.get_active() == True:
        output = output.resize((int(width / 8), int(height / 8)))

    output.save("fractal.png", "PNG")

    headerBar.set_subtitle("Ready")
    progressThrobber.stop()

    while Gtk.events_pending():
        Gtk.main_iteration()

    mainViewport.set_from_file("fractal.png")

class Handler:
    def onDestroy(self, *args):
        quit()
        Gtk.main_quit()

    def executeButtonPressed(self, button):
        headerBar.set_subtitle("Processing...")
        progressThrobber.start()

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

    def viewExternallyPressed(self, button):
        output = Image.open("fractal.png")
        output.show()

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
progressThrobber = builder.get_object("progressThrobber")
supersamplingCheck = builder.get_object("supersamplingCheck")
hypersamplingCheck = builder.get_object("supersampling4Check")
ubersamplingCheck = builder.get_object("supersampling8Check")
viewExternally = builder.get_object("viewExternally")

mainViewport.set_from_file("logo.png")

window = builder.get_object("mainWindow")
window.show_all()
Gtk.main()
