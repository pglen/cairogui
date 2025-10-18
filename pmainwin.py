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
        #self.geom = self.window.get_geometry()

    def add_widget(self,widget):
        self.children.append(widget)

    def defproc(self, e):
        #print("main:", e)
        ret = False
        if 1: #while 1:
            if e.type == X.ButtonPress:
                if self.d.get_input_focus().focus != e.window:
                    e.window.set_input_focus(X.RevertToParent, X.CurrentTime )
                    #print("focus change:", self.d.get_input_focus().focus,
                    #       "child:", e.window)

            # Main window has been destroyed, quit
            if e.type == X.DestroyNotify:
                print("Exit destroy", e) #, self.window)
                if e.window == self.window:
                    #sys.exit(0)
                    ret = True

            for aa in self.children:
                try:
                    if e.window == aa.window :
                        processed = aa.pevent(e)
                        #print("ret:", ret)
                        if processed:
                            continue
                except:
                    pass
                    #print("ch", sys.exc_info())
            #print("after children:", len(self.children))

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
                        print("Exit client prot")
                        sys.exit(0)
                        ret = True
                        #break

            # Left button pressed, start to draw
            if e.type == X.ButtonPress:
                pass

            # Left button released, finish drawing
            if e.type == X.ButtonRelease:
                pass

            # Mouse movement with button pressed, draw
            if e.type == X.MotionNotify:
                pass

            ret = self.keyhandler(e)

            #break

        return ret

    def keyhandler(self, e):

        ''' Form keys '''

        if e.type == X.KeyPress:
            keysym = self.d.keycode_to_keysym(e.detail, 0)
            was = self.keyh.handle_modkey(e, keysym)
            if not was:
                print("state:", hex(e.state), "key:", hex(keysym), str(self.keyh))

            if  self.keyh.alt and keysym == XK_x:
                #print("ALT_X")
                ret = True
                sys.exit(0)

            if  keysym == XK_Tab:
                #print("tab")
                oldfoc = 0
                for cnt, aa in enumerate(self.children):
                    if self.d.get_input_focus().focus == aa.window:
                        #print("focus", aa.window)
                        oldfoc = aa
                        break
                if not oldfoc:
                    #print("was NO oldfoc")
                    cnt = 0
                else:
                    #print("was oldfoc", cnt)
                    if self.keyh.shift:
                        cnt -= 1
                    else:
                        cnt += 1

                # Cycle to previous / next
                for _ in range(len(self.children)):
                    if cnt < 0:         # Wrap around
                        cnt = 0
                    if cnt >= len(self.children):
                        cnt = 0
                    if self.children[cnt].config.nofocus:
                        #print("skip", self.children[cnt].config.text)
                        if self.keyh.shift:
                            cnt -= 1
                        else:
                            cnt += 1
                # Cy
                    else:
                        break

                self.children[cnt].window.set_input_focus \
                                (X.RevertToParent, X.CurrentTime )

        if e.type == X.KeyRelease:
            #print("main keyrelease", e, e.detail)
            keysym = self.d.keycode_to_keysym(e.detail, 0) #e.state & 0x1)
            was = self.keyh.handle_modkey(e, keysym)
            if not was:
                print("rele", hex(keysym), str(self.keyh))


# EOF
