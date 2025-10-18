#!/usr/bin/python

import  sys, time

''' Widgets '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *

from PIL import Image, ImageDraw, ImageFont

from pguibase import BaseWindow, Makefont, pConfig, KeyState

class pButton(BaseWindow):

    def __init__(self, config, args = None):

        if args.verbose:
            print("pButton.__init__", config)
        self.pressed = 0
        self.config  = config
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

    def draw_font(self, text, offsx = 0, offsy = 0):

        ''' Draw proportional font ; clear background '''

        self.draw.rectangle((0, 0, self.size[0], self.size[1]), self.gray)
        self.draw.text((self.pressed + offsx, self.pressed + offsy), text, fill="black",
                                font=self.font.font, anchor="la")
        self.window.put_pil_image(self.gc,
                                    self.config.border, self.config.border,
                                            self.image)
    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.draw_font(self.config.text)
        #self.gc.change(foreground = self.ddgray)
        self.draw_foc()

    def _enterstate(self):
        self.window.change_attributes(background_pixel=self.lgray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self.draw_font(self.config.text)
        #self.gc.change(foreground = self.llgray)
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
            if self.config.callme:
                self.config.callme(self)

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

        self.keyh = KeyState()
        self.config  = config
        self.pressed = 0
        self.font = Makefont(config.font_name, config.font_size, args)
        self.size = self.font.get_size(self.config.text)
        self.csize = self.font.get_realsize("W")
        config.www, config.hhh = self.size
        config.www += 3 * config.border + self.csize[0]
        config.hhh += 2 * config.border
        super().__init__(config, args)
        self.geom = self.window.get_geometry()
        self.image = Image.new("RGB", self.size, self.gray)
        self.draw = ImageDraw.Draw(self.image)
        self.geom = self.window.get_geometry()
        self._defstate()

    def _checkout(self):

        top = 2 * self.geom.height // 8
        butt = 4 * self.geom.height // 8
        self.gc.change(foreground = self.gray)
        self.window.fill_rectangle(self.gc, top, top, butt, butt)

        self.gc.change(foreground = self.black)
        self.gc.change(line_width=2)
        self.window.rectangle(self.gc, top, top, butt, butt)
        #print("Checked:", self.config.checked)
        if self.config.checked:
            base = self.config.border
            self.window.poly_line(self.gc, X.CoordModeOrigin,
                [
                (top + base, top +  base),
                (butt - base, top + butt - base),
                (top + butt -  base, top + base)
                ])

    def draw_font(self, text, offsx = 0, offsy = 0):

        ''' Draw proportional font ; clear background '''

        self.draw.rectangle((0, 0, self.size[0], self.size[1]), self.gray)
        self.draw.text((self.pressed, self.pressed), text, fill="black",
                                font=self.font.font, anchor="la")
        self.window.put_pil_image(self.gc, 2 * self.config.border + offsx,
                                        self.config.border + offsy, self.image)

    def _defstate(self):
        self.draw_font(self.config.text, self.csize[0])
        self._checkout();
        #self.gc.change(foreground = self.gray)
        self.draw_foc()

    def _enterstate(self):
        self.draw_font(self.config.text, self.csize[0])
        self._checkout();
        #self.gc.change(foreground = self.gray)
        self.draw_foc()

    def pevent(self, e):
        #print("in check event:", e)
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
            self._defstate()
            got = True

        if e.type == X.FocusOut:
            self._defstate()
            got = True

        if e.type == X.ButtonPress:
            got = True

        if e.type == X.ButtonRelease:
            self.config.checked = not self.config.checked
            self._enterstate()
            if self.config.callme:
                self.config.callme(self)
            got = True

        if e.type == X.KeyPress:
            keysym = self.d.keycode_to_keysym(e.detail, 0)
            was = self.keyh.handle_modkey(e, keysym)
            if keysym == XK_space:
                self.config.checked = not self.config.checked
                self._defstate()
            got = True

        if e.type == X.KeyRelease:
            #print("check keyrelease", e)
            got = True

        return got

class pRadio(BaseWindow):

    def __init__(self, config, args):

        ''' Radio button '''

        if args.verbose:
            print("pRadio.__init__", config)

        self.keyh = KeyState()
        self.config  = config
        self.pressed = 0

        self.font = Makefont(config.font_name, config.font_size, args)
        self.size = self.font.get_size(self.config.text)
        self.csize = self.font.get_realsize("W")
        config.www, config.hhh = self.size
        config.www += 3 * config.border + self.csize[0]
        config.hhh += 2 * config.border

        super().__init__(config, args)
        self.geom = self.window.get_geometry()

        self.image = Image.new("RGB", self.size, self.gray)
        self.draw = ImageDraw.Draw(self.image)
        self.geom = self.window.get_geometry()
        self._defstate()

    def _radioout(self):
        self.gc.change(foreground = self.black)
        self.gc.change(line_width=1)
        self.window.arc(self.gc,
                    self.geom.height // 4, self.geom.height // 4,
                        2 * self.geom.height // 4, 2 * self.geom.height // 4,
                        0, 360 * 64)
        if self.config.checked:
            base = 2 * self.config.border # + 2
            self.window.fill_arc(self.gc,
                self.geom.height // 4 + 4, self.geom.height // 4 + 4,
                    2 * self.geom.height // 4 - 8,
                        2 * self.geom.height // 4 - 8,
                        0, 360 * 64)

    def draw_font(self, text, offsx = 0, offsy = 0):

        ''' Draw proportional font ; clear background '''

        self.draw.rectangle((0, 0, self.size[0], self.size[1]), self.gray)
        self.draw.text((self.pressed, self.pressed), text, fill="black",
                                font=self.font.font, anchor="la")
        self.window.put_pil_image(self.gc, 2 * self.config.border + offsx,
                                        self.config.border + offsy, self.image)
    def _defstate(self):
        self.window.change_attributes(background_pixel=self.gray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self._radioout();
        self.draw_font(self.config.text, self.csize[0])
        self.draw_foc()

    def _enterstate(self):
        self.window.change_attributes(background_pixel=self.gray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self._radioout();
        self.draw_font(self.config.text, self.csize[0])
        #self.gc.change(foreground = self.gray)
        self.draw_foc()

    def pevent(self, e):
        #print("in check event:", e)
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
            self._defstate()
            got = True

        if e.type == X.FocusOut:
            self._defstate()
            got = True

        if e.type == X.ButtonPress:
            got = True

        if e.type == X.ButtonRelease:
            #self.pressed = 0
            self.config.checked = not self.config.checked
            self._enterstate()
            if self.config.callme:
                self.config.callme(self)
            got = True

        if e.type == X.KeyPress:
            keysym = self.d.keycode_to_keysym(e.detail, 0)
            was = self.keyh.handle_modkey(e, keysym)
            if keysym == XK_space:
                print("checked", self.config.checked)
                self.config.checked = not self.config.checked
                self._defstate()
            got = True

        if e.type == X.KeyRelease:
            #print("check keyrelease", e)
            got = True

        return got

class pLabel(BaseWindow):

    def __init__(self, config, args):

        ''' Static Label '''

        if args.verbose:
            print("pLabel.__init__", config)

        self.config  = config
        self.pressed = 0

        self.font = Makefont(config.font_name, config.font_size, args)
        self.size = self.font.get_size(self.config.text)
        self.csize = self.font.get_realsize("W")
        config.www, config.hhh = self.size
        config.www += 2 * config.border
        config.hhh += 2 * config.border

        super().__init__(config, args)
        self.geom = self.window.get_geometry()

        self.image = Image.new("RGB", self.size, self.gray)
        self.draw = ImageDraw.Draw(self.image)
        self.geom = self.window.get_geometry()
        self._defstate()

    def draw_font(self, text, offsx = 0, offsy = 0):

        ''' Draw proportional font ; clear background '''

        self.draw.rectangle((0, 0, self.size[0], self.size[1]), self.gray)
        self.draw.text((self.pressed, self.pressed), text, fill="black",
                                font=self.font.font, anchor="la")
        self.window.put_pil_image(self.gc, 2 * self.config.border + offsx,
                                        self.config.border + offsy, self.image)
    def _defstate(self):
        self.draw_font(self.config.text)

    def _enterstate(self):
        self.draw_font(self.config.text)

    def pevent(self, e):
        got = 0
        if e.type == X.CreateNotify:
            got = True

        if e.type == X.EnterNotify:
            #self._enterstate()
            got = True

        if e.type == X.LeaveNotify:
            #self._defstate()
            got = True

        if e.type == X.ButtonPress:
            got = True

        if e.type == X.ButtonRelease:
            got = True

        if e.type == X.KeyPress:
            #print("check keypress", e)
            got = True

        if e.type == X.KeyRelease:
            #print("check keyrelease", e)
            got = True

        return got

# EOF
