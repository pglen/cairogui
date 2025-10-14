#!/usr/bin/python

import  sys, time

sys.path.append("python_xlib")

import  Xlib
from    Xlib import display, Xutil, ext
from    Xlib.keysymdef.latin1 import *

event_maskx =  (    Xlib.X.ExposureMask |
                    Xlib.X.StructureNotifyMask |
                    Xlib.X.SubstructureNotifyMask |
                    Xlib.X.SubstructureRedirectMask |
                    Xlib.X.ButtonPressMask |
                    Xlib.X.ButtonReleaseMask |
                    #Xlib.X.Button1MotionMask |
                    Xlib.X.PointerMotionMask |
                    Xlib.X.PointerMotionHintMask |
                    Xlib.X.KeyPressMask |
                    Xlib.X.KeyReleaseMask |
                    Xlib.X.EnterWindowMask |
                    Xlib.X.LeaveWindowMask |
                    Xlib.X.ResizeRedirectMask |
                    Xlib.X.PropertyChangeMask |
                    Xlib.X.VisibilityChangeMask |
                    Xlib.X.CWEventMask |
                    Xlib.X.FocusChangeMask )

class BaseWindow(object):

    ''' Base for all '''

    def __init__(self, display, parent, xx, yy, www, hhh, border = 0):

        self.d = display
        self.objects = []
        #self.texts = []
        #self.texts.append("Hello")
        self.entered = False
        #self.width = 10
        #self.height = 10
        self.screen = self.d.screen()

        self.colormap = self.screen.default_colormap

        self.white  = self.colormap.alloc_color(0xffff, 0xffff, 0xffff).pixel
        self.blue   = self.colormap.alloc_color(0x4fff, 0x4fff, 0xffff).pixel
        self.green  = self.colormap.alloc_color(0x4fff, 0xffff, 0x4fff).pixel
        self.red    = self.colormap.alloc_color(0xffff, 0x4fff, 0x4fff).pixel
        self.black  = self.colormap.alloc_color(0x0000, 0x0000, 0x0000).pixel

        self.llgray = self.colormap.alloc_color(0xefff, 0xefff, 0xefff).pixel
        self.lgray  = self.colormap.alloc_color(0xdfff, 0xdfff, 0xdfff).pixel
        self.gray   = self.colormap.alloc_color(0xcfff, 0xcfff, 0xcfff).pixel
        self.dgray  = self.colormap.alloc_color(0xbfff, 0xbfff, 0xbfff).pixel
        self.ddgray = self.colormap.alloc_color(0xafff, 0xafff, 0xafff).pixel

        #print("lookup", self.colormap.lookup_color("green"))

        # Find which screen to open the window on
        #print("screen", self.screen)

        #self.root = self.screen.root
        #self.HELLO_WORLD = self.d.intern_atom(b'HELLO_WORLD')

        self.window = parent.create_window(
            xx, yy, www, hhh,
            0,   # we take over border,
            self.screen.root_depth,
            Xlib.X.InputOutput,
            Xlib.X.CopyFromParent,
            background_pixel = self.gray, #screen.white_pixel,
            event_mask = event_maskx,
            colormap = Xlib.X.CopyFromParent,
            #keys = {'backing_store': Xlib.X.NotUseful, 'all_event_masks': 1980679760, }
            )

        #print("exts", self.d.list_extensions())
        old = self.d.get_font_path()
        old.append("/usr/share/fonts/opentype")
        print("fonts", old)
        #self.d.set_font_path(old)
        #newp = self.d.get_font_path()

        font_name = "fixed-medium"
        font_size = 18
        fontx = "*%s*--%d*" % (font_name, font_size)
        #fontx = "*"
        #print("fontx", fontx)
        #self.lll = self.d.list_fonts_with_info(fontx, 100)
        self.lll = self.d.list_fonts(fontx, 100)
        #for aa in self.lll:
        #    print(aa)
        #XFontStruct *font = XLoadQueryFont(dpy, font_name);
        self.font = self.d.open_font(self.lll[0])

        self.gc = self.window.create_gc(
            foreground = self.blue, # self.screen.black_pixel,
            background = self.blue, # self.screen.white_pixel,
            font=self.font,
            line_width=1,
            #line_style=Xlib.X.LineOnOffDash,
            #cap_style=Xlib.X.CapRound,
            #join_style=Xlib.X.JoinMiter
            #join_style=Xlib.X.JoinRound
            #join_style=Xlib.X.JoinBevel
            )
        #self.gc.change(line_width=5)
        #self.window.change_attributes(border_pixel=self.dgray, border_width=5) # Set border to red and 5 pixels wide
        #self.d.flush()
        #print(self.window.get_attributes())

        #self.window.change_attributes(event_mask=event_maskx)
        #self.window.change_attributes(backing_store=0)
        #ext.shape.select_input(self.d, True)

        # Set some WM info
        self.WM_PROTOCOLS = self.d.intern_atom('WM_PROTOCOLS')

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
        self.window.map()
        self.geom = self.window.get_geometry()
        #print("geom", self.geom)

    def invalidate(self, window = None):

        ggg = self.window.get_geometry()
        event = Xlib.protocol.event.Expose(
            window=self.window,
            x=0, y=0,
            width=ggg.width,
            height=ggg.height,
            count=0 # Indicates this is the last expose event
            )
        # Send the event to the window
        window.send_event(event, propagate=False)
        #Xlib.display.flush()

class pButton(BaseWindow):

    def __init__(self, display, parent, text, xx, yy, www, hhh, border = 0):

        #print("pButton.__init__", text, border)

        self.border = border
        if type(text) != type(b""):
            self.text = text.encode()
        else:
            self.text = text
        font_name = "fixed-medium"
        font_size = 18
        fontx = "*%s*--%d*" % (font_name, font_size)
        #fontx = "*"
        #print("fontx", fontx)
        #self.lll = self.d.list_fonts_with_info(fontx, 100)
        self.lll = display.list_fonts(fontx, 100)
        #for aa in self.lll:
        #    print(aa)
        font = display.open_font(self.lll[0])
        self.te = font.query_text_extents(self.text)
        #print("te", te)
        nhhh = self.te.font_ascent + self.te.font_descent + 4 * border
        nwww = self.te.overall_width + 4 * border
        super().__init__(display, parent, xx, yy, nwww, nhhh, border)
        self.geom = self.window.get_geometry()
        self.gc.change(line_width=self.border)
        self.pressed = 0
        self._defstate()

        #self.gc.change(foreground = self.screen.black_pixel)
        #te = self.gc.query_text_extents(text)
        self._textout()
        #self.invalidate(self.window)
        #print("gc:", dir(self.gc.query))
        #te = self.gc.query()
        #print("fff", te._data['char_infos'][0])
        #print("te len:", len(ddd))
        #for aa in te._data['char_infos']:
        #    print("te:", aa['character_width'], end = " " )

    def _textout(self):
        self.gc.change(foreground = self.screen.black_pixel)
        self.window.draw_text(self.gc, 2 * self.border + self.pressed,
                    self.te.font_ascent + 2 * self.border + self.pressed,
                         self.text)

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.gc.change(foreground = self.ddgray)
        self.window.rectangle(self.gc, 0, 0, self.geom.width-1, self.geom.height-1)
        self._textout();

    def _focstate(self):
        self.window.change_attributes(background_pixel=self.gray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self.gc.change(foreground = self.llgray)
        self.window.rectangle(self.gc, self.pressed, self.pressed,
                                self.geom.width-1, self.geom.height-1)
        self._textout();
        #self.invalidate(self.window)

    def pevent(self, e):
        #print("in pbutton event:", e)
        got = 0
        if e.type == Xlib.X.CreateNotify:
            got = True

        if e.type == Xlib.X.EnterNotify:
            self._focstate()
            got = True

        if e.type == Xlib.X.LeaveNotify:
            self._defstate()
            got = True

        if e.type == Xlib.X.ButtonPress:
            self.pressed = 1
            self._focstate()
            print("pbutt mousepress", e)

        if e.type == Xlib.X.ButtonRelease:
            self.pressed = 0
            self._focstate()
            print("pbutt mouserelease", e)

        if e.type == Xlib.X.KeyPress:
            print("pbutt keypress", e)
            got = True

        if e.type == Xlib.X.KeyRelease:
            print("pbutt keyrelease", e)
            got = True


        return got

class MainWindow(BaseWindow):

    def __init__(self, display, parent , xx, yy, www, hhh):
        super().__init__(display, parent, xx, yy, www, hhh)

        self.children = []
        child = pButton(self.d, self.window, b"Hello World",
                        www//4, hhh//4, www//2, hhh//2, border = 4)
        self.children.append(child)
        child.window.map()

    # Main loop, handling events
    def winloop(self):
        current = None
        while 1:
            e = self.d.next_event()
            if e.type == Xlib.X.ButtonPress:
                if self.d.get_input_focus().focus != e.window:
                    e.window.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime )
                    print("focus change:", self.d.get_input_focus().focus, "child:", e.window)
            for aa in self.children:
                if e.window == aa.window :
                    processed = aa.pevent(e)
                    #print("ret:", ret)
                    if processed:
                        continue

            if e.type == Xlib.X.MotionNotify:
                #print("Motion", end = " ")
                pass
            else:
                #print(" **** Event", e)
                pass

            if e.type == Xlib.X.ClientMessage:
                if e.client_type == self.WM_PROTOCOLS:
                    fmt, data = e.data
                    if fmt == 32 and data[0] == self.WM_DELETE_WINDOW:
                        #print("Exit client prot")
                        break
                        #sys.exit(0)

            # Window has been destroyed, quit
            if e.type == Xlib.X.DestroyNotify:
                print("Exit dest")
                break
                #sys.exit(0)

            #continue

            # Some part of the window has been exposed,
            # redraw all the objects.
            if e.type == Xlib.X.Expose:
                pass
                #if e.count == 0:
                #    self.window.fill_rectangle(self.gc, 0, 0, 60, 60)

                #print("****Expose", e)
                #for oo in self.objects:
                #    oo.expose(e)
                #for tt in self.texts:
                #    print(tt)

            # Left button pressed, start to draw
            if e.type == Xlib.X.ButtonPress and e.detail == 1:
                pass
                #self.gc.change(foreground = self.screen.black_pixel)
                #self.window.draw_text(self.gc, 10, 10, b"Hello, world!")
                #self.window.poly_line(self.gc, Xlib.X.CoordModeOrigin,
                #                [(20, 20), (100, 100), (120, 150)], )
                #self.invalidate(self.window)

            # Left button released, finish drawing
            if e.type == Xlib.X.ButtonRelease and e.detail == 1 and current:
                pass
                #current.finish(e)
                #current = None

            # Mouse movement with button pressed, draw
            if e.type == Xlib.X.MotionNotify and current:
                #current.motion(e)
                pass

            if e.type == Xlib.X.KeyPress:
                #print("main keypress: ", dir(e), e._data)
                if  e.state & Xlib.X.Mod1Mask and e.detail ==  self.d.keysym_to_keycode(XK_x):
                    print("ALT_X")
                    sys.exit(0)

            if e.type == Xlib.X.KeyRelease:
                print("main keyrelease", e)

        # Exit
        print("Exited loop.")

