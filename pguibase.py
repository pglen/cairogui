#!/usr/bin/python

import  sys, time

''' Widgets '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *
from    Xlib.keysymdef.miscellany import *

from PIL import Image, ImageDraw, ImageFont

#fontx = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# Web Safe Fonts:
#    Arial (sans-serif)
#    Verdana (sans-serif)
#    Tahoma (sans-serif)
#    Trebuchet MS (sans-serif)
#    Times New Roman (serif)
#    Georgia (serif)
#    Garamond (serif)
#    Courier New (monospace)
#    Brush Script MT (cursive)

gl_font = None
#global gl_font
#        if not gl_font:
#            gl_font = fontInfo(fontx, 24)

# These are the fonts; order them as preferred
fontx = (   "OpenSans-Regular", "DejaVuSans", "Verdana", "Arial",
            "Roboto-Medium", "Georgia", "Times_New_Roman",
            "Trebuchet_MS", "Courier_New", "")

class Makefont(object):

    ''' Create common font object for all widgets, measure it '''

    def __init__(self, fontname, size, args = None):

        self.font = None ; self.te = None
        cnt = 0

        # Try command line font first
        try:
            fname = fontname
            self.font = ImageFont.truetype(fontname, size=size)
        except: pass

        if not self.font:
            while True:
                fname = fontx[cnt]
                if not fname:
                    break
                try:
                    #print("Try:", fontname)
                    self.font = ImageFont.truetype(fname, size=size)
                except:
                    #print(sys.exc_info())
                    pass
                if self.font:
                    break
                cnt += 1
                if cnt >= len(fontx):
                    break
        if not self.font:
            raise OSError("No font found. Tried: %s" % str(fontx))
        self.te   = self.font.getmetrics()
        if args.verbose:
            print("Got font:", fname)
        gl_font = self

    def get_size(self, text):

        ''' Get font size, Fake ascent / descent '''

        font_width, font_height = self.font.getsize(text)
        fake_width, fake_height = self.font.getsize("Ag")
        return font_width, fake_height

    def get_realsize(self, text):

        font_width, font_height = self.font.getsize(text)
        return font_width, font_height

class pConfig(object):

    ''' Configuration to pass to display elements '''

    _font_name = "fixed-medium"
    _font_size = 18
    _border = 4

    def __init__(self, disp, window):
        self.display = disp
        self.parent = window
        self.font_name = ""  #pConfig._font_name
        self.font_size = 18 #pConfig._font_size
        self.border  = pConfig._border
        self.text  = "Empty"
        self.xx  = 2
        self.yy  = 2
        self.www = 20
        self.hhh = 20
        self.callme = None
        self.name = "UnNamed"
        self.checked = True
        self.nofocus = False

    def __str__(self):
        return "font='%s' xx=%d yy=%d www=%d hhh=%d text='%s'" % \
                (self.font_name, self.xx, self.yy,
                    self.www, self.hhh, self.text)

event_maskx =  (
        X.ExposureMask | X.StructureNotifyMask | X.SubstructureNotifyMask |
        X.SubstructureRedirectMask | X.ButtonPressMask | X.ButtonReleaseMask |
        X.PointerMotionMask | X.PointerMotionHintMask | X.KeyPressMask |
        X.KeyReleaseMask |  X.EnterWindowMask | X.LeaveWindowMask |
        X.ResizeRedirectMask | X.PropertyChangeMask | X.VisibilityChangeMask |
        X.CWEventMask | X.FocusChangeMask )

class BaseWindow(object):

    ''' Base for all widgets '''

    def __init__(self, config, args):

        if args.verbose:
            print("basewindow", config)

        self.d = config.display
        self.screen = self.d.screen()

        self.objects = []
        self.entered = False

        #self.texts = []
        #self.texts.append("Hello")
        #self.width = 10
        #self.height = 10

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

        self.window = config.parent.create_window(
            config.xx, config.yy, config.www, config.hhh,
            0,   # we take over border,
            self.screen.root_depth,
            X.InputOutput,
            X.CopyFromParent,
            background_pixel = self.gray, #screen.white_pixel,
            event_mask = event_maskx,
            colormap = X.CopyFromParent,
            )

        self.gc = self.window.create_gc(
            foreground = self.blue, # self.screen.black_pixel,
            background = self.blue, # self.screen.white_pixel,
            #font=self.font.font,
            line_width=1,
            #line_style=X.LineOnOffDash,
            #cap_style=X.CapRound,
            #join_style=X.JoinMiter
            #join_style=X.JoinRound
            #join_style=X.JoinBevel
            )
        self.window.map()
        self.geom = self.window.get_geometry()
        #print("geom", self.geom)

    def invalidate(self, window = None):

        ggg = self.window.get_geometry()
        event = protocol.event.Expose(
            window=self.window,
            x=0, y=0,
            width=ggg.width,
            height=ggg.height,
            count=0 # Indicates this is the last expose event
            )
        # Send the event to the window
        window.send_event(event, propagate=False)
        #Xlib.display.flush()

    def draw_foc(self):

        if self.d.get_input_focus().focus == self.window:
            self.gc.change(line_style=X.LineOnOffDash)
            self.gc.change(foreground = self.ddgray)
        else:
            self.gc.change(line_style=X.LineSolid)
            self.gc.change(foreground = self.gray)

        self.window.rectangle(self.gc, 0, 0,
                        self.geom.width-1, self.geom.height-1)
        self.gc.change(line_style=X.LineSolid)
        self.gc.change(foreground = self.gray)

class   KeyState(object):

    def __init__(self):

        self.shift = False;
        self.ctrl = False;
        self.alt = False;

        self.lshift = False;
        self.rshift = False;
        self.lctrl = False;
        self.rctrl = False;
        self.lalt = False;
        self.ralt = False;

        self.caps = False;
        self.super = False;

    def __str__(self):

        return  " shift:"  + str(self.shift) + \
                " ctrl:"   + str(self.ctrl) + \
                " alt:"    + str(self.alt) + \
                " super:"  + str(self.super)

                # rshift:" + str(self.rshift) + \
                #" rctrl:"  + str(self.rctrl) + \
                #" ralt:"   + str(self.ralt)

    def handle_modkey(self, e, keysym):

        #print("modkey:", hex(keysym))
        was = 0
        if e.type == 2:
            if keysym == XK_Alt_L:
                self.alt = True ;  self.lalt = True ; was = True
            if keysym == XK_Alt_R:
                self.alt = True ;  self.ralt = True ;  was = True
            if keysym == XK_Control_L:
                self.ctrl = True ;  self.lctrl = True ; was = True
            if keysym == XK_Control_R:
                self.ctrl = True ;  self.rctrl = True ; was = True
            if keysym == XK_Shift_L:
                self.shift = True ;  self.rshift = True ; was = True
            if keysym == XK_Shift_R:
                self.shift = True ;  self.rshift = True ; was = True
            if keysym == XK_Super_L:
                self.super = True ;  was = True
            if keysym == XK_Super_R:
                self.super = True ;  was = True

            if keysym == XK_Caps_Lock:
                self.caps = not self.caps
                self.shift = self.caps ;

        if e.type == 3:
            if keysym == XK_Alt_L:
                self.alt = False ; self.lalt = False ; was = True
            if keysym == XK_Alt_R:
                self.alt = False ; self.ralt = False ; was = True
            if keysym == XK_Control_L:
                self.ctrl = False;  self.lctrl = False  ;  was = True
            if keysym == XK_Control_R:
                self.ctrl = False;  self.rctrl = False ;  was = True
            if keysym == XK_Shift_L:
                self.shift = False;  self.lshift = False ;  was = True
            if keysym == XK_Shift_R:
                self.shift = False;  self.rshift = False ;  was = True
            if keysym == XK_Super_L:
                self.super = False ;  was = True

        return was


# EOF