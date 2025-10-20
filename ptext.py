#!/usr/bin/python

import  sys, time

''' Widgets '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *

from PIL import Image, ImageDraw, ImageFont

from pguibase import BaseWindow, Makefont, pConfig, KeyState
from pwidgets import BaseWindow
from pyutils import *

from    Xlib.keysymdef.latin1 import *
from    Xlib.keysymdef.miscellany import *

class pText(BaseWindow):

    def __init__(self, config, args):

        #print("pButton.__init__", display, parent, "text:", text,
        #                    xx, yy, "callme", callme, "border", border)

        self.config = config
        self.border = self.config.border
        self.curx = 0 ; self.cury = 0
        self.font = Makefont(config.font_name, config.font_size, args)
        self.size = self.font.get_size(self.config.text)

        super().__init__(config, args)
        self.charsize = self.font.get_size("a")
        self.keyh = KeyState()
        self.geom = self.window.get_geometry()
        self.gc.change(line_width=self.border)
        self.image = Image.new("RGB", (self.config.www, self.config.hhh), self.gray)
        self.draw = ImageDraw.Draw(self.image)
        self.pressed = 0
        self._defstate()

    def currline(self):
        linex = ""
        for cnt, line in enumerate(self.config.text.split()):
            #print("line", cnt, line, self.cury)
            if cnt == self.cury:
                #print(self.cury, cnt, line)
                linex = line
        return linex

    def pos2offs(self):
        linex = ""; offs = 0
        for cnt, line in enumerate(self.config.text.split()):
            #print("line", cnt, line, self.cury)
            if cnt == self.cury:
                break
            offs += len(line) + 1   # Placeholder for new line
        offs += self.curx
        #print("line offs:", offs)
        return offs

    def draw_font(self, text, offsx = 0, offsy = 0):

        ''' Draw proportional font ; clear background '''

        if not self.config.text:
            return

        self.draw.rectangle((0, 0, self.config.www, self.config.hhh), self.white)
        xxx = self.curx * self.charsize[0]
        yyy = self.cury * self.charsize[1]
        linex = self.currline()
        # Calculate line offset:
        posx = 0
        for cnt, aa in enumerate(linex):
            sss = self.font.get_size(aa)
            #print("aa", aa, sss)
            if cnt >= self.curx:
                break
            posx += sss[0]
        #print("curr", linex, self.curx, "posx", posx)
        try:
            sss =  self.font.get_size(linex[self.curx])
        except:
            sss =  self.font.get_size("a")
        #print("sss", sss)
        self.draw.rectangle((posx, yyy + self.charsize[1],
                             posx + sss[0], yyy + self.charsize[1] + 2,
                            ), self.black)

        self.draw.text((self.pressed + offsx, self.pressed + offsy),
                              text, fill="black",
                                font=self.font.font, anchor="la")
        self.window.put_pil_image(self.gc, self.config.border, self.config.border,
                                            self.image)

    def _defstate(self):
        self.window.change_attributes(background_pixel = self.white)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)

        self.gc.change(foreground = self.dgray)
        if self.d.get_input_focus().focus == self.window:
            self.gc.change(line_style=X.LineOnOffDash)
        else:
            self.gc.change(line_style=X.LineSolid)

        self.window.rectangle(self.gc, 0, 0, self.geom.width-1, self.geom.height-1)
        self.draw_font(self.config.text)

    def _focstate(self):
        self.gc.change(foreground = self.dgray)
        if self.d.get_input_focus().focus == self.window:
            self.gc.change(line_style=X.LineOnOffDash)
        else:
            self.gc.change(line_style=X.LineSolid)

        self.window.rectangle(self.gc, self.pressed, self.pressed,
                                self.geom.width-1, self.geom.height-1)
        self.draw_font(self.config.text)

        #self.invalidate(self.window)

    def pevent(self, e):
        try:
            self.peventw(e)
        except:
            #print("\nevent err:", sys.exc_info())
            print_exc()

    def peventw(self, e):

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
            #self.pressed = 1
            self._focstate()
            #print("pbutt mousepress", e)

        if e.type == X.ButtonRelease:
            #self.pressed = 0
            self._focstate()
            #print("pbutt mouserelease", e)
            if self.config.callme:
                self.config.callme(self)

        if e.type == X.FocusIn:
            print("ptext focusIn", e)
            self._defstate()
            got = True

        if e.type == X.FocusOut:
            print("ptext focusOut", e)
            self._defstate()
            got = True

        if e.type == X.KeyPress:
            #print("ptext keypress", e)
            # Keystate translation is only valid for shift
            keysym = self.d.keycode_to_keysym(e.detail, e.state & 0x3)
            sss = str(chr(keysym))
            #print("keysym:", keysym, sss)
            if e.state & 0x2:
                if  sss.islower():
                    #print("capslock LOW")
                    keysym -= 0x20
                elif  sss.isupper():
                    #print("capslock HIGH")
                    keysym += 0x20

            was = self.keyh.handle_modkey(e, keysym)
            if not was:
                redraw = False
                ccc = chr(keysym)
                #print("ptext char:", keysym, chr(keysym))
                if keysym == XK_Left:
                    #print("left arrow")
                    if self.curx > 0:
                        self.curx -= 1
                    else:
                        linex = self.currline()
                        if self.cury > 0:
                            self.cury -= 1
                            linex = self.currline()
                            self.curx = len(linex)
                    redraw = True
                elif keysym == XK_Right:
                    #print("right arrow")
                    linex = self.currline()
                    if self.curx  < len(linex):
                        self.curx += 1
                    else:
                        self.curx  = 0
                        self.cury += 1
                    redraw = True
                elif keysym == XK_Up:
                    #print("up arrow")
                    if self.cury:
                        self.cury -= 1
                        redraw = True
                elif keysym == XK_Down:
                    #print("down arrow")
                    self.cury += 1
                    redraw = True
                elif keysym == XK_BackSpace:
                    if self.curx == 0:
                        if self.cury > 0:
                            self.cury -= 1
                            linex = self.currline()
                            self.curx = len(linex)
                            posx = self.pos2offs()
                            tmptxt = self.config.text[:posx]
                            tmptxt += self.config.text[posx+1:]
                            self.config.text = tmptxt
                    else:
                        posx = self.pos2offs()
                        tmptxt = self.config.text[:posx]
                        tmptxt += self.config.text[posx+1:]
                        self.config.text = tmptxt
                        self.curx -= 1
                    redraw = True

                elif ccc.isprintable():
                    redraw = True
                    if keysym == XK_Return:
                        #self.config.text += "\r"
                        self.config.text += "\n"
                        self.cury += 1
                        self.curx =  0
                    else:
                        posx = self.pos2offs()
                        tmptxt = self.config.text[:posx]
                        tmptxt += chr(keysym)
                        tmptxt += self.config.text[posx:]
                        self.config.text = tmptxt
                        self.curx += 1
                if redraw:
                    self.draw_font(self.config.text)
                #print("coord", self.curx, self.cury, self.pos2offs())
            got = True

        if e.type == X.KeyRelease:
            #print("ptext keyrelease", e)
            got = True

        return got

# EOF
