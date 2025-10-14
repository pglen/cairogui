#!/usr/bin/python

import  sys, time
import argparse

#sys.path.append("python_xlib")

import  Xlib
from    Xlib import display, Xutil, ext
from    Xlib.keysymdef.latin1 import *

from pwidgets import pCheck, pLabel, pButton, MainWindow

def args():
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Display text using X11')
    parser.add_argument('--text', help='Text to display')
    parser.add_argument('--fg-color', default='white',
                       help='Text color (white/black or hex color like #FFBB00)')
    parser.add_argument('--bg-color', default='black',
                       help='Background color (white/black or hex color like #000000)')
    parser.add_argument('--font', type=str,
                       default='-misc-fixed-medium-r-normal--13-120-75-75-c-70-iso8859-1',
                       help='X11 font name')
    args = parser.parse_args()

def callme(butt):
    print("Button pressed", butt.text)

class mainwin(MainWindow):

    def __init__(self, disp, xx, yy, width, height):
        super().__init__(disp, disp.screen().root, xx, yy, width, width)

        basex = width//4 ; basey = 32
        ttt = b"Button %d Press"
        child = None #pButton(self.d, self.window, ttt, basex, basey, callme)
        #self.add_widget(child)

        for aa in range(4):
            # Add buttons
            if not child:
                offs = 0
            else:
                offs = (child.geom.height + 4) * aa
            child = pButton(self.d, self.window, ttt % aa, basex,
                                basey + offs, callme)
            self.add_widget(child)

        child = pLabel(self.d, self.window, "Hello Label:", 4, 4)
        self.add_widget(child)

        child = pCheck(self.d, self.window, "Check Label", basex, 200)
        self.add_widget(child)

    def winloop(self):
        #print("Winloop")
        while 1:
            e = self.d.next_event()
            ret = self.defproc(e)
            if ret:
                break
        # Exit
        print("Exited loop.")

# Define window dimensions and position
x, y, width, height = 100, 100, 300, 200

if __name__ == "__main__":

    # Establish a connection to the X server
    try:
        disp = display.Display()
    except:
        print("Cannot open display.")
        sys.exit(1)

    win = mainwin(disp, x, y, width, height)
    win.winloop()
    # Close the display connection
    disp.close()

# EOF
