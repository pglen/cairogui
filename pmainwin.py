#!/usr/bin/python

import  sys, time

''' Main window '''

from    Xlib import X, display, Xutil, ext, protocol, XK
from    Xlib.keysymdef.latin1 import *
from    Xlib.keysymdef.miscellany import *

from PIL import Image, ImageDraw, ImageFont

from pguibase import BaseWindow, Makefont, pConfig, KeyState

class MainWindow(BaseWindow):

    def __init__(self, config, args):
        self.config = config
        self.args = args

        super().__init__(config, args)
        self.children = []
        self.keyh = KeyState()

        #print("args", self.args)

        #self.gc.change(line_width=3)
        #self.window.fill_arc(self.gc, 30, 30, 20, 20, 10, 100 )
        #self.window.rectangle(self.gc, 50, 50, 20, 20)

        # Set some WM info
        self.WM_PROTOCOLS = self.d.intern_atom('WM_PROTOCOLS')

        self.window.set_wm_name(config.name)
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
        while 1:
            e = self.d.next_event()
            ret = self.defproc()
            if ret:
                break

    def defproc(self, e):
        ret = False
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
                print("Exit destoy")
                ret = True
                break
                #sys.exit(0)

            # Left button pressed, start to draw
            if e.type == X.ButtonPress and e.detail == 1:
                pass

            # Left button released, finish drawing
            if e.type == X.ButtonRelease:
                pass

            # Mouse movement with button pressed, draw
            if e.type == X.MotionNotify:
                pass

            ret = self.keyhandler(e)

            break

        return ret

    def keyhandler(self, e):

        if e.type == X.KeyPress:
            keysym = self.d.keycode_to_keysym(e.detail, 0)
            was = self.keyh.handle_modkey(e, keysym)
            if not was:
                print("state:", hex(e.state), "key:", hex(keysym), str(self.keyh))

            if  self.keyh.alt and keysym == XK_x:
                print("ALT_X")
                ret = True
                sys.exit(0)

            if  keysym == XK_Tab:
                print("tab")

        if e.type == X.KeyRelease:
            #print("main keyrelease", e, e.detail)
            keysym = self.d.keycode_to_keysym(e.detail, 0) #e.state & 0x1)
            was = self.keyh.handle_modkey(e, keysym)
            if not was:
                print("rele", hex(keysym), str(self.keyh))


# EOF
