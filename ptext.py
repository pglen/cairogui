#!/usr/bin/python

import  sys, time

''' Widgets '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *

from pwidgets import BaseWindow

class pText(BaseWindow):

    def __init__(self, disp, config):

        #print("pButton.__init__", display, parent, "text:", text,
        #                    xx, yy, "callme", callme, "border", border)

        self.config = config
        self.callme = self.config.callme
        self.border = self.config.border
        if type(config.text) != type(b""):
            self.config.text = config.text.encode()

        font_name = "fixed-medium"
        font_name = "times"
        font_size = 14
        fontx = "*%s*--%d*" % (font_name, font_size)
        #fontx = "*"
        #print("fontx", fontx)
        #self.lll = self.d.list_fonts_with_info(fontx, 100)
        self.lll = disp.list_fonts(fontx, 100)
        #for aa in self.lll:
        #    print(aa)
        font = disp.open_font(self.lll[0])
        self.te = font.query_text_extents(self.config.text)
        #print("te", te)
        #nhhh = self.te.font_ascent + self.te.font_descent + 4 * self.border
        #nwww = self.te.overall_width + 4 * self.border

        super().__init__(disp, config.parent, config.xx, config.yy,
                                   config.www, config.hhh, config.border)
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
        self.window.draw_text(self.gc, 2 * self.border,
                    self.te.font_ascent + 2 * self.border,
                         self.config.text)

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.white)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)

        self.gc.change(foreground = self.dgray)
        if self.d.get_input_focus().focus == self.window:
            self.gc.change(line_style=X.LineOnOffDash)
        else:
            self.gc.change(line_style=X.LineSolid)

        self.window.rectangle(self.gc, 0, 0, self.geom.width-1, self.geom.height-1)
        self._textout();

    def _focstate(self):
        self.gc.change(foreground = self.dgray)
        if self.d.get_input_focus().focus == self.window:
            self.gc.change(line_style=X.LineOnOffDash)
        else:
            self.gc.change(line_style=X.LineSolid)

        self.window.rectangle(self.gc, self.pressed, self.pressed,
                                self.geom.width-1, self.geom.height-1)
        self._textout();

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

        if e.type == X.FocusIn:
            print("ptext focusIn", e)
            self._defstate()
            got = True

        if e.type == X.FocusOut:
            print("ptext focusOut", e)
            self._defstate()
            got = True

        if e.type == X.KeyPress:
            print("ptext keypress", e)
            got = True

        if e.type == X.KeyRelease:
            print("ptext keyrelease", e)
            got = True

        return got

