#!/usr/bin/python

import  os, sys, time
import  argparse
import  threading

# Try local Xlib copy from source (worked the same)
#sys.path = ["python_xlib",] + sys.path
from    Xlib import X, display, Xutil, ext

#import xcffib

#print("file:", X.__file__)

if __name__ == "__main__":

    # Establish a connection to the X server
    try:
        disp = display.Display()
    except:
        print("Cannot open display.")
        sys.exit(1)

    old = disp.get_font_path()
    print("old font:", old)
    #ddd = "/usr/share/fonts/"
    #for aa in os.listdir(ddd):
    #    dddd = ddd + aa
    #    if os.path.isdir(dddd):
    #        #print("aa", dddd)
    #        old.append(dddd)
    #print("\nold font2:", old)
    #disp.set_font_path(old)
    #print("After set")
    #time.sleep(1)
    #newp = disp.get_font_path()
    #print("new font:", newp)

    lll = disp.list_fonts("*", 10000)
    #lll = disp.list_fonts_with_info(b"*misc*", 100)
    for aa in lll:
        print(aa)

    #font = disp.open_font(lll[0])
    #print("font:", dir(font))
    #print("font:", font.__font__())
    #qqq = font.query()
    #print("qqq:", qqq._data['min_bounds'])
    #for aa in qqq._data:
    #    print("attr:", qqq)
    #font_info = XLoadQueryFont(dpy,
    #                           "-*-nimbus*-medium-r-*-*-12-*-*-*-m-*-iso8859-1");

    import freetype
    face = freetype.Face("DejaVuSans.ttf")
    face.set_char_size( 48*64 )
    face.load_char('S')
    bitmap = face.glyph.bitmap
    print(bitmap.buffer)

    # Close the display connection
    disp.close()
