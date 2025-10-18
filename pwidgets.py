#!/usr/bin/python

import  sys, time

''' Widgets '''

from    Xlib import X, display, Xutil, ext, protocol
from    Xlib.keysymdef.latin1 import *

from PIL import Image, ImageDraw, ImageFont

from pguibase import BaseWindow, Makefont, pConfig, KeyState

def tooltip(oconf, args, e):

    print("tooltip", e)
    config = pConfig(oconf.display, oconf.display.screen().root)
    config.font_size = max(args.fontsize // 2, 14)
    config.font_name = args.fontname
    config.text = " Tooltip Here " + oconf.text * 3
    #config.nofocus = True
    #config.checked = True
    #config.callme = checkchange
    config.xx = oconf.xx + 4
    config.yy = oconf.yy + 4
    config.border = 6
    child = pLabel(config, args)
    #child.window.set_wm_hints(flags = Xutil.StateHint,
    #                             initial_state = Xutil.NormalState)
    #child.window.set_wm_normal_hints(
	#		flags=(Xutil.PPosition | Xutil.PSize | Xutil.PMinSize),
	#		min_width=50,
	#		min_height=50
	#		)

    # Get atoms for window types and states
    wm_window_type = disp.intern_atom('_NET_WM_WINDOW_TYPE')
    wm_window_type_utility = disp.intern_atom('_NET_WM_WINDOW_TYPE_UTILITY') # For tool windows
    wm_state = disp.intern_atom('_NET_WM_STATE')
    wm_state_above = disp.intern_atom('_NET_WM_STATE_ABOVE') # To keep it on top
    wm_state_skip_taskbar = disp.intern_atom('_NET_WM_STATE_SKIP_TASKBAR') # To hide from taskbar

    # Set the window type to utility (tool window)
    child.window.change_property(
        wm_window_type,
        Xatom.ATOM,
        32, # 32-bit property
        [wm_window_type_utility]
    )

    # Set window state to "above" and "skip taskbar"
    child.window.change_property(
        wm_state,
        Xatom.ATOM,
        32,
        [wm_state_above, wm_state_skip_taskbar]
    )


    return child

class pButton(BaseWindow):

    def __init__(self, config, args = None):

        if args.verbose:
            print("pButton.__init__", config)

        self.keyh = KeyState()
        self.pressed = 0
        self.config  = config
        self.args  = args
        self.font = Makefont(config.font_name, config.font_size, args)
        self.size = self.font.get_size(self.config.text)
        self.toolwin = None
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
        self.window.put_pil_image(self.gc, self.config.border, self.config.border,
                                            self.image)
    def _defstate(self):
        self.window.change_attributes(background_pixel = self.dgray)
        self.window.clear_area(0, 0, self.geom.width, self.geom.height)
        self.draw_font(self.config.text)
        self.draw_foc()

    def _enterstate(self):
        self.window.change_attributes(background_pixel=self.lgray)
        self.window.clear_area(0, 0, self.geom.width-1, self.geom.height-1)
        self.draw_font(self.config.text)
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
            #if self.toolwin:
            #    print("close", self.toolwin.window)
            #    self.toolwin.window.destroy()
            #    self.toolwin = False
            self._defstate()
            got = True
        if e.type == X.FocusIn:
            self._defstate()
            got = True
        if e.type == X.FocusOut:
            #self.toolwin.window.destroy()
            #self.toolwin = False
            self._defstate()
            got = True
        if e.type == X.ButtonPress:
            #print("pbutt", e)
            if e.detail == 1:
                self.pressed = 1
                self._enterstate()
            if e.detail == 3:
                #print("pbutt R mousepress", e)
                if self.toolwin:
                    self.toolwin.window.destroy()
                self.toolwin = tooltip(self.config, self.args, e)

            got = True
        if e.type == X.ButtonRelease:
            #print("pbutt", e)
            if e.detail == 1:
                self.pressed = 0
                self._defstate()
                if self.config.callme:
                    self.config.callme(self)
            got = True

        if e.type == X.KeyPress:
            keysym = self.d.keycode_to_keysym(e.detail, 0)
            was = self.keyh.handle_modkey(e, keysym)
            if keysym == XK_space:
                self.pressed = 1
                self.config.checked = not self.config.checked
                self._defstate()
            got = True

        if e.type == X.KeyRelease:
            keysym = self.d.keycode_to_keysym(e.detail, 0)
            was = self.keyh.handle_modkey(e, keysym)
            if keysym == XK_space:
                self.pressed = 0
                self._defstate()
                if self.config.callme:
                    self.config.callme(self)
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
                if self.config.callme:
                    self.config.callme(self)
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

class   Tooltip(BaseWindow):
        pass


# EOF
