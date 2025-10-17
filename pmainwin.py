#!/usr/bin/python

import  sys, time

''' Main window '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *

from PIL import Image, ImageDraw, ImageFont

from pguibase import BaseWindow, Makefont, pConfig

class MainWindow(BaseWindow):

    def __init__(self, config, args):
        self.config = config
        self.args = args

        super().__init__(config, args)
        self.children = []

        #print("args", self.args)

        #self.gc.change(line_width=3)
        #self.window.fill_arc(self.gc, 30, 30, 20, 20, 10, 100 )
        #self.window.rectangle(self.gc, 50, 50, 20, 20)

# Set some WM info
        #self.WM_PROTOCOLS = self.d.intern_atom('WM_PROTOCOLS')

        self.window.set_wm_name('Xlib example: window.py')
        #self.window.set_wm_icon_name('draw.py')
        #self.window.set_wm_class('Example', 'XlibExample')

        self.WM_DELETE_WINDOW = self.d.intern_atom('WM_DELETE_WINDOW')
        self.window.set_wm_protocols([self.WM_DELETE_WINDOW])
        self.window.set_wm_hints(flags = Xutil.StateHint,
                                 initial_state = Xutil.NormalState)

        #self.window.set_wm_normal_hints(flags = (Xutil.PPosition | Xutil.PSize
        #                                         | Xutil.PMinSize),
        #                                min_width = 20,
        #                                min_height = 20)

        #print(self.window.list_properties())

        # Map the window, making it visible
        #self.geom = self.window.get_geometry()

    def add_widget(self,widget):
        self.children.append(widget)

    # Main loop, handling events
    def defloop(self):
        current = None
        while 1:
            e = self.d.next_event()
            self.defproc()

    def defproc(self, e):
        current = None ; ret = False
        while 1:
            if e.type == X.ButtonPress:
                if self.d.get_input_focus().focus != e.window:
                    e.window.set_input_focus(X.RevertToParent, X.CurrentTime )
                    #print("focus change:", self.d.get_input_focus().focus,
                    #       "child:", e.window)
            for aa in self.children:
                if e.window == aa.window :
                    processed = aa.pevent(e)
                    #print("ret:", ret)
                    if processed:
                        continue

            if e.type == X.MotionNotify:
                #print("Motion", end = " ")
                pass
            else:
                #print(" **** Event", e)
                pass

            if e.type == X.ClientMessage:
                if e.client_type == self.WM_PROTOCOLS:
                    fmt, data = e.data
                    if fmt == 32 and data[0] == self.WM_DELETE_WINDOW:
                        #print("Exit client prot")
                        ret = True
                        break
                        #sys.exit(0)

            # Window has been destroyed, quit
            if e.type == X.DestroyNotify:
                print("Exit dest")
                ret = True
                break
                #sys.exit(0)

            #continue

            # Some part of the window has been exposed,
            # redraw all the objects.
            if e.type == X.Expose:
                pass
                #if e.count == 0:
                #    self.window.fill_rectangle(self.gc, 0, 0, 60, 60)

                #self.gc.change(line_width=3)
                #self.window.arc(self.gc, 30, 30, 20, 20, 0, 360 * 64 )
                #self.window.rectangle(self.gc, 50, 50, 20, 20)
                #
                #print("****Expose", e)
                #for oo in self.objects:
                #    oo.expose(e)
                #for tt in self.texts:
                #    print(tt)

            # Left button pressed, start to draw
            if e.type == X.ButtonPress and e.detail == 1:
                pass
                #self.gc.change(foreground = self.screen.black_pixel)
                #self.window.draw_text(self.gc, 10, 10, b"Hello, world!")
                #self.window.poly_line(self.gc, X.CoordModeOrigin,
                #                [(20, 20), (100, 100), (120, 150)], )
                #self.invalidate(self.window)

            # Left button released, finish drawing
            if e.type == X.ButtonRelease and e.detail == 1 and current:
                pass
                #current.finish(e)
                #current = None

            # Mouse movement with button pressed, draw
            if e.type == X.MotionNotify and current:
                #current.motion(e)
                pass

            if e.type == X.KeyPress:
                #print("main keypress: ", dir(e), e._data)
                if  e.state & X.Mod1Mask and e.detail == \
                     self.d.keysym_to_keycode(XK_x):
                    print("ALT_X")
                    ret = True
                    #sys.exit(0)

            if e.type == X.KeyRelease:
                print("main keyrelease", e)
            break
        return ret

