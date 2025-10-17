#!/usr/bin/python

import  sys, time

''' Widgets '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *

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

    ''' Create common font object for all widgets '''

    def __init__(self, fontname, size):

        self.font = None ; self.te = None
        cnt = 0

        #global gl_font
        #if gl_font:
        #    self = gl_font
        #    return

        while True:
            fontname = fontx[cnt]
            if not fontname:
                break
            try:
                #print("Try:", fontname)
                self.font = ImageFont.truetype(fontname, size=size)
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
        gl_font = self

    def get_size(self, text):

        ''' Get font size, Fake ascent / descent '''

        font_width, font_height = self.font.getsize(text)
        fake_width, fake_height = self.font.getsize("Ag")
        return font_width, fake_height

class pConfig(object):

    ''' Configuration to pass to display elements '''

    _font_name = "fixed-medium"
    _font_size = 18
    _border = 4

    def __init__(self, disp, window):
        self.display = disp
        self.parent = window
        self.font_name = pConfig._font_name
        self.font_size = pConfig._font_size
        self.border  = pConfig._border
        self.text  = ""
        self.x  = 0
        self.y  = 0
        self.www = 10
        self.hhh = 10
        self.callme = None

    def __str__(self):
        return "font='%s' x=%d y=%d www=%d hhh=%d" % \
                (self.font_name, self.x, self.y, self.www, self.hhh)

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
            #keys = {'backing_store': X.NotUseful, 'all_event_masks': 1980679760, }
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

