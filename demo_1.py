#!/usr/bin/python

import  sys, time
import  argparse
import  threading

# Try local Xlib copy from source (worked the same)
sys.path = ["python_xlib",] + sys.path

from    Xlib import X, display, Xutil, ext
from    Xlib.keysymdef.latin1 import *

#print("file:", X.__file__)

from pguibase import BaseWindow, pConfig
from pwidgets import pConfig, pRadio, pCheck, pButton
from pmainwin import MainWindow
from ptext import pText

def argsfunc():
    # Add argument parsing
    parser = argparse.ArgumentParser(description='GUI toolkit')
    parser.add_argument('-v', '--verbose', action="store_true", help='Verbosity level')
    parser.add_argument('--text', help='Text to display')
    parser.add_argument('--fg-color', default='white',
                       help='Text color (white/black or hex color like #FFBB00)')
    parser.add_argument('--bg-color', default='black',
                       help='Background color (white/black or hex color like #000000)')
    parser.add_argument('--fontname', type=str,
                       default='DejaVuSans',
                       help='Font name')
    parser.add_argument('--fontsize', type=int,
                       default=18,
                       help='Font size')
    parser.add_argument('--width', type=int,
                       default=500,
                       help='Window size')
    parser.add_argument('--height', type=int,
                       default=400,
                       help='Window size')
    args = parser.parse_args()
    return args

def callb(butt, delay=1):
    print("Button thread pressed", butt.text)
    #time.sleep(delay)
    #print("Button thread pressed done", butt.text)
    pass

def callme(butt):
    #t = threading.Thread(target=callb, args=(butt,), kwargs={"delay": 2})
    #t.start()
    print("Button pressed done", butt.text)

#pconfig = pConfig()

class mainwin(MainWindow):

    def __init__(self, disp, xx, yy, width, height, args):

        config = pConfig(disp, disp.screen().root)
        config.xx = config.yy = 10
        config.www = width ; config.hhh = height
        config.text = "Main "

        super().__init__(config, args)

        #child = pLabel(self.d, self.window, "Hello Label:", 6, 6)
        #self.add_widget(child)

        basex = 24 ; basey = 32
        child = None
        offs = 8
        config = pConfig(disp, self.window)
        config.xx = basex ; config.yy = 22
        config.www = 250  ; config.hhh = 150
        config.font_size = args.fontsize
        config.font_name = args.fontname

        # Add buttons
        for aa in range(2):
            config.text = "Button %d Here" % (aa + 1)
            if child:
                #offs = (child.geom.height + 14) * (aa )
                config.yy += child.geom.height + 6
            child = pButton(config, args)
            self.add_widget(child)

        config2 = pConfig(disp, self.window)
        config2.font_size = args.fontsize
        config2.font_name = args.fontname
        config2.text = "Checkbox"
        config2.xx = basex ; config2.yy = 170
        child = pCheck(config2, args)
        self.add_widget(child)

        #
        #child = pRadio(self.d, self.window, "Radio button",  basex, 170, callme)
        #self.add_widget(child)
        #
        #config = pConfig()
        #config.parent = self.window
        #config.xx = basex
        #config.yy = 220
        #config.www = 250
        #config.hhh = 150
        #config.text = "Text Editor"
        #
        #child = pText(self.d, config)
        #self.add_widget(child)

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
x, y = 100, 100;

if __name__ == "__main__":

    # Establish a connection to the X server
    try:
        disp = display.Display()
    except:
        print("Cannot open display.")
        sys.exit(1)

    args = argsfunc()

    #print("exts", self.d.list_extensions())
    # Add fonts
    #old = disp.get_font_path()
    #old.append("/usr/share/fonts/X11/100dpi")
    #print("old font:", old)
    #disp.set_font_path(old)
    #newp = disp.get_font_path()
    #print("new font:", newp)

    win = mainwin(disp, x, y, args.width, args.height, args)
    win.winloop()
    # Close the display connection
    disp.close()

# EOF
