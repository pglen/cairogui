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

# These are the fonts; order them as preferred
fontx = (   "OpenSans-Regular", "DejaVuSans", "Verdana", "Arial",
            "Roboto-Medium", "Georgia", "Times_New_Roman",
            "Trebuchet_MS", "Courier_New", "")

class fontinfo(object):

    ''' Create common font object for all widgets '''

    def __init__(self, fontname, size):

        self.font = None ; self.te = None
        cnt = 0

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

        print("Got:", fontname)
        self.te   = self.font.getmetrics()

    def get_size(self, text):

        ''' Size '''

        if type(b"") == type(text):
            text2 = text.decode()
        else:
            text2 = text
        font_width, font_height = self.font.getsize(text2)
        return font_width, font_height

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

    def __init__(self, config, args = None):

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

class pButton(BaseWindow):

    def __init__(self, config, args = None):

        if args.verbose:
            print("pButton.__init__", config)

        self.config = config
        self.callme = config.callme
        if type(config.text) != type(b""):
            self.text = config.text.encode()
        else:
            self.text = config.text
        self.checked = False

        global gl_font
        if not gl_font:
            gl_font = fontinfo(fontx, 24)
        self.font = gl_font

        self.size = self.font.get_size(self.config.text)
        config.www, config.hhh = self.size
        config.www += 2 * config.border
        config.hhh += 2 * config.border

        super().__init__(config, args)
        self.geom = self.window.get_geometry()
        self.gc.change(line_width=self.config.border)
        self.pressed = 0
        self.image = Image.new("RGB", (self.size[0], self.size[1]), self.gray)
        self.draw = ImageDraw.Draw(self.image)
        self._defstate()

    def draw_font(self, text):

        ''' Draw proportional font '''

        if type(b"") == type(text):
            text2 = text.decode()
        else:
            text2 = text
        self.draw.text((self.pressed, self.pressed), text2, fill="black", font=self.font.font)
        self.window.put_pil_image(self.gc, 0, 0, self.image)

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.draw_font(self.text)
        self.gc.change(foreground = self.ddgray)

        if self.d.get_input_focus().focus == self.window:
            self.gc.change(line_style=X.LineOnOffDash)
        else:
            self.gc.change(line_style=X.LineSolid)

        self.window.rectangle(self.gc, 0, 0, self.geom.width-1, self.geom.height-1)

    def _focstate(self):
        self.window.change_attributes(background_pixel=self.gray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self.draw_font(self.text)
        self.gc.change(foreground = self.llgray)

        if self.d.get_input_focus().focus == self.window:
            self.gc.change(line_style=X.LineOnOffDash)
        else:
            self.gc.change(line_style=X.LineSolid)

        self.window.rectangle(self.gc, self.pressed, self.pressed,
                                self.geom.width-1, self.geom.height-1)
        #self._textout();
        #self.invalidate(self.window)

    def pevent(self, e):
        #print("in pbutton event:", e)
        got = 0
        if e.type == X.CreateNotify:
            got = True

        if e.type == X.EnterNotify:
            self._focstate()
            got = True

        if e.type == X.LeaveNotify:
            self._defstate()
            got = True

        if e.type == X.FocusIn:
            print("ptext focusIn", e)
            self._defstate()
            got = True

        if e.type == X.FocusOut:
            print("ptext focusOut", e)
            self._defstate()
            got = True

        if e.type == X.ButtonPress:
            self.pressed = 1
            self._focstate()
            #print("pbutt mousepress", e)

        if e.type == X.ButtonRelease:
            self.pressed = 0
            self._focstate()
            #print("pbutt mouserelease", e)
            if self.callme:
                self.callme(self)

        if e.type == X.KeyPress:
            print("pbutt keypress", e)
            got = True

        if e.type == X.KeyRelease:
            print("pbutt keyrelease", e)
            got = True

        return got

class pCheck(BaseWindow):

    def __init__(self, display, parent, text, xx, yy, callme=None, border=4):

        #print("pButton.__init__", display, parent, "text:", text,
        #                    xx, yy, "callme", callme, "border", border)

        self.checked = True
        self.callme = callme
        self.border = border
        if type(text) != type(b""):
            self.text = text.encode()
        else:
            self.text = text

        font = init_widget_font(display)
        self.te = font.query_text_extents(self.text)
        #print("te", te)
        nhhh = self.te.font_ascent + self.te.font_descent + 4 * self.border
        nwww = self.te.overall_width + 4 * self.border + 2 * self.te.font_ascent + self.te.font_descent
        super().__init__(display, parent, xx, yy, nwww, nhhh, self.border)
        self.geom = self.window.get_geometry()
        self.gc.change(line_width=self.border)
        self.pressed = 0
        #self._defstate()
        self._focstate()

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

    def _checkout(self):
        self.gc.change(foreground = self.black)
        self.gc.change(line_width=1)
        self.window.rectangle(self.gc,
                    self.geom.height // 4, self.geom.height // 4,
                        2 * self.geom.height // 4, 2 * self.geom.height // 4)
        if self.checked:
            base = 2 * self.border # + 2
            self.window.poly_line(self.gc, X.CoordModeOrigin,
                        [
                        (base + 2, base + self.te.font_descent + 2),
                        (base + self.te.font_ascent // 2, base + self.te.font_ascent ),
                        (base + self.te.font_ascent, base + self.te.font_descent),
                         ])

    def _textout(self):
        self.gc.change(foreground = self.screen.black_pixel)
        self.window.draw_text(self.gc, self.geom.height + 2 * self.border + self.pressed,
                    self.te.font_ascent + 2 * self.border + self.pressed,
                         self.text)

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.gc.change(foreground = self.ddgray)
        #self.window.rectangle(self.gc, 0, 0, self.geom.width-1, self.geom.height-1)
        self._textout();
        self._checkout();

    def _focstate(self):
        self.window.change_attributes(background_pixel=self.gray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        #self.gc.change(foreground = self.llgray)
        #self.window.rectangle(self.gc, self.pressed, self.pressed,
        #                        self.geom.width-1, self.geom.height-1)
        self._textout();
        self._checkout();
        #self.invalidate(self.window)

    def pevent(self, e):
        #print("in check event:", e)
        got = 0
        if e.type == X.CreateNotify:
            got = True

        if e.type == X.EnterNotify:
            self._focstate()
            got = True

        if e.type == X.LeaveNotify:
            #self._defstate()
            got = True

        if e.type == X.ButtonPress:
            got = True

        if e.type == X.ButtonRelease:
            #self.pressed = 0
            if self.callme:
                self.callme(self)
            self.checked = not self.checked
            self._focstate()
            self.invalidate(self.window)
            #print("check mouserelease", e, self.checked)
            got = True

        if e.type == X.KeyPress:
            print("check keypress", e)
            got = True

        if e.type == X.KeyRelease:
            print("check keyrelease", e)
            got = True

        return got

class pRadio(BaseWindow):

    def __init__(self, display, parent, text, xx, yy, callme=None, border=4):

        #print("pButton.__init__", display, parent, "text:", text,
        #                    xx, yy, "callme", callme, "border", border)

        self.checked = True
        self.callme = callme
        self.border = border
        if type(text) != type(b""):
            self.text = text.encode()
        else:
            self.text = text
        font = init_widget_font(display)
        self.te = font.query_text_extents(self.text)
        #print("te", te)
        nhhh = self.te.font_ascent + self.te.font_descent + 4 * self.border
        nwww = self.te.overall_width + 4 * self.border + 2 * self.te.font_ascent + self.te.font_descent
        super().__init__(display, parent, xx, yy, nwww, nhhh, self.border)
        self.geom = self.window.get_geometry()
        self.gc.change(line_width=self.border)
        self.pressed = 0
        self._focstate()
        self._textout()

    def _radioout(self):
        self.gc.change(foreground = self.black)
        self.gc.change(line_width=1)

        #print("arc", self.geom.height // 2, self.geom.height // 2,
        #        self.geom.height // 2, self.geom.height // 2,)

        self.window.arc(self.gc,
                    self.geom.height // 4, self.geom.height // 4,
                        2 * self.geom.height // 4, 2 * self.geom.height // 4,
                        0, 360 * 64)

        if self.checked:
            base = 2 * self.border # + 2
            self.window.fill_arc(self.gc,
                self.geom.height // 4 + 4, self.geom.height // 4 + 4,
                    2 * self.geom.height // 4 - 8, 2 * self.geom.height // 4 - 8,
                        0, 360 * 64)

    def _textout(self):
        self.gc.change(foreground = self.screen.black_pixel)
        self.window.draw_text(self.gc, self.geom.height + 2 * self.border + self.pressed,
                    self.te.font_ascent + 2 * self.border + self.pressed,
                         self.text)

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.gc.change(foreground = self.ddgray)
        #self.window.rectangle(self.gc, 0, 0, self.geom.width-1, self.geom.height-1)
        self._textout();
        self._checkout();

    def _focstate(self):
        self.window.change_attributes(background_pixel=self.gray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        #self.gc.change(foreground = self.llgray)
        #self.window.rectangle(self.gc, self.pressed, self.pressed,
        #                        self.geom.width-1, self.geom.height-1)
        self._textout();
        self._radioout();
        #self.invalidate(self.window)

    def pevent(self, e):
        #print("in check event:", e)
        got = 0
        if e.type == X.CreateNotify:
            got = True

        if e.type == X.EnterNotify:
            self._focstate()
            got = True

        if e.type == X.LeaveNotify:
            #self._defstate()
            got = True

        if e.type == X.ButtonPress:
            got = True

        if e.type == X.ButtonRelease:
            #self.pressed = 0
            if self.callme:
                self.callme(self)
            self.checked = not self.checked
            self._focstate()
            self.invalidate(self.window)
            #print("check mouserelease", e, self.checked)
            got = True

        if e.type == X.KeyPress:
            print("check keypress", e)
            got = True

        if e.type == X.KeyRelease:
            print("check keyrelease", e)
            got = True

        return got

'''

class pLabel(BaseWindow):

    def __init__(self, display, parent, text, xx, yy, border=0):

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
        nhhh = self.te.font_ascent + self.te.font_descent + 4 * self.border
        nwww = self.te.overall_width + 4 * self.border
        #super().__init__(display, parent, xx, yy, nwww, nhhh, self.border)
        #self.geom = self.window.get_geometry()
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
        #self.window.change_attributes(background_pixel = self.dgray)
        #self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        #self.gc.change(foreground = self.ddgray)
        #self.window.rectangle(self.gc, 0, 0, self.geom.width-1, self.geom.height-1)
        #self._textout();
        pass

    def pevent(self, e):
        #print("in label event:", e)
        pass
'''

class MainWindow(BaseWindow):

    def __init__(self, config, args):
        self.config = config
        self.args = args
        super().__init__(config, args)
        self.children = []

        print("args", self.args)

        #self.gc.change(line_width=3)
        #self.window.fill_arc(self.gc, 30, 30, 20, 20, 10, 100 )
        #self.window.rectangle(self.gc, 50, 50, 20, 20)

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
                    #print("focus change:", self.d.get_input_focus().focus, "child:", e.window)
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
                if  e.state & X.Mod1Mask and e.detail ==  self.d.keysym_to_keycode(XK_x):
                    print("ALT_X")
                    ret = True
                    #sys.exit(0)

            if e.type == X.KeyRelease:
                print("main keyrelease", e)
            break
        return ret

# EOF
