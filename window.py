#!/usr/bin/python

import  sys, time

sys.path.append("python_xlib")

import  Xlib
from    Xlib import display, Xutil, ext
from    Xlib.keysymdef.latin1 import *

from pwidgets import pButton, MainWindow

#print (Xlib.__file__)

# Establish a connection to the X server
disp = display.Display()

# Define window dimensions and position
x, y, width, height = 100, 100, 300, 200

if __name__ == "__main__":

    import argparse
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Display text using X11')
    parser.add_argument('--text', help='Text to display')
    parser.add_argument('--fg-color', default='white',
                       help='Text color (white/black or hex color like #FFBB00)')
    parser.add_argument('--bg-color', default='black',
                       help='Background color (white/black or hex color like #000000)')
    parser.add_argument('--delay', type=int, default=3,
                       help='Display for n seconds')
    parser.add_argument('--font', type=str,
                       default='-misc-fixed-medium-r-normal--13-120-75-75-c-70-iso8859-1',
                       help='X11 font name')
    args = parser.parse_args()

    win = MainWindow(disp, disp.screen().root, x, y, width, height)
    win.winloop()

    # Close the display connection
    disp.close()

# EOF
