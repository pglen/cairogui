#!/usr/bin/python

import  sys, time

''' Widgets '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *

from PIL import Image, ImageDraw, ImageFont

from pguibase import BaseWindow, Makefont, pConfig

class pButton(BaseWindow):

    def __init__(self, config, args = None):

        if args.verbose:
            print("pButton.__init__", config)
        self.pressed = 0
        self.checked = False
        self.config  = config
        self.callme  = config.callme
        self.text    = config.text
        self.font = Makefont(config.font_name, config.font_size, args)
        self.size = self.font.get_size(self.config.text)
        config.www, config.hhh = self.size

        config.www += 2 * config.border
        config.hhh += 2 * config.border

        super().__init__(config, args)
        #time.sleep(1)
        self.geom = self.window.get_geometry()

        self.gc.change(line_width=self.config.border)
        self.image = Image.new("RGB", (self.size[0], self.size[1]), self.gray)
        self.draw = ImageDraw.Draw(self.image)
        self._defstate()

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.draw_font(self.text)
        self.gc.change(foreground = self.ddgray)
        self.draw_foc()

    def _enterstate(self):
        self.window.change_attributes(background_pixel=self.lgray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self.draw_font(self.text)
        self.gc.change(foreground = self.llgray)

        self.draw_foc()

    def pevent(self, e):
        #print("in pbutton event:", e)
        got = 0
        if e.type == X.CreateNotify:
            got = True

        if e.type == X.EnterNotify:
            self._enterstate()
            got = True

        if e.type == X.LeaveNotify:
            self._defstate()
            got = True

        if e.type == X.FocusIn:
            #print("ptext focusIn", e)
            self._defstate()
            got = True

        if e.type == X.FocusOut:
            #print("ptext focusOut", e)
            self._defstate()
            got = True

        if e.type == X.ButtonPress:
            self.pressed = 1
            self._enterstate()
            #print("pbutt mousepress", e)

        if e.type == X.ButtonRelease:
            self.pressed = 0
            self._enterstate()
            #print("pbutt mouserelease", e)
            if self.callme:
                self.callme(self)

        if e.type == X.KeyPress:
            #print("pbutt keypress", e)
            got = True

        if e.type == X.KeyRelease:
            #print("pbutt keyrelease", e)
            got = True

        return got

class pCheck(BaseWindow):

    ''' Check button '''

    def __init__(self, config, args):

        if args.verbose:
            print("pCheck.__init__", config)

        self.pressed = 0
        self.checked = True
        self.config  = config
        self.callme  = config.callme
        self.text    = config.text

        self.font = Makefont(config.font_name, config.font_size, args)
        self.size = self.font.get_size(self.config.text)
        config.www, config.hhh = self.size
        config.www += + self.size[1]
        super().__init__(config, args)

        #self.image = Image.new("RGB", (self.size[0], self.size[1]), self.gray)
        self.image = Image.new("RGB", (config.www, config.hhh), self.gray)
        self.draw = ImageDraw.Draw(self.image)
        self.geom = self.window.get_geometry()
        self._defstate()

    def _checkout(self):
        self.gc.change(foreground = self.black)
        self.gc.change(line_width=1)
        self.window.rectangle(self.gc,
                    self.geom.height // 4, self.geom.height // 4,
                        2 * self.geom.height // 4, 2 * self.geom.height // 4)
        if self.checked:
            base = 2 * self.config.border # + 2
            self.window.poly_line(self.gc, X.CoordModeOrigin,
                [
                (base + 2, base  + 2),
                (base +  12 // 2, base  ),
                (base + 12, base ),
                 ])

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.gc.change(foreground = self.ddgray)
        self.draw_font(self.text, self.size[1]) #, 0, self.geom.height)
        self._checkout();

    def _enterstate(self):
        self.window.change_attributes(background_pixel=self.gray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self.draw_font(self.text, self.size[1])
        self._checkout();

    def pevent(self, e):
        #print("in check event:", e)
        got = 0
        if e.type == X.CreateNotify:
            got = True

        if e.type == X.EnterNotify:
            self._enterstate()
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
            self._enterstate()
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

    ''' Radio button '''

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
        self._enterstate()
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
                    2 * self.geom.height // 4 - 8,
                        2 * self.geom.height // 4 - 8,
                        0, 360 * 64)

    def _textout(self):
        self.gc.change(foreground = self.screen.black_pixel)
        self.window.draw_text(self.gc,
            self.geom.height + 2 * self.border + self.pressed,
                    self.te.font_ascent + 2 * self.border + self.pressed,
                         self.text)

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.gc.change(foreground = self.ddgray)
        self._textout();
        self._checkout();

    def _enterstate(self):
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
            self._enterstate()
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
            self._enterstate()
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


# EOF
