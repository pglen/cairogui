class pButton(BaseWindow):

    def __init__(self, display, parent, text, xx, yy, www, hhh, border = 0):

        self.border = border
        self.text = text
        font_name = "fixed-medium"
        font_size = 18
        fontx = "*%s*--%d*" % (font_name, font_size)
        #fontx = "*"
        #print("fontx", fontx)
        #self.lll = disp.list_fonts_with_info(fontx, 100)
        self.lll = disp.list_fonts(fontx, 100)
        #for aa in self.lll:
        #    print(aa)
        #XFontStruct *font = XLoadQueryFont(dpy, font_name);
        font = disp.open_font(self.lll[0])

        self.te = font.query_text_extents(text)
        #print("te", te)
        nhhh = self.te.font_ascent + self.te.font_descent + 2 * border
        nwww = self.te.overall_width + 2 * border

        super().__init__(display, parent, xx, yy, nwww, nhhh, border)
        self.geom = self.window.get_geometry()

        #self.window.change_attributes(border_pixel=self.dgray, border_width=5) # Set border to red and 5 pixels wide
        self.window.change_attributes(background_pixel=self.dgray)
        #self.window.clear_area(0, 0, self.geom.width, self.geom.height)

        self.gc.change(foreground = self.screen.black_pixel)
        #te = self.gc.query_text_extents(text)
        #self.window.draw_text(self.gc, 0, self.te.font_ascent, text)
        self._textout()
        self.invalidate(self.window)

        #print("gc:", dir(self.gc.query))
        #te = self.gc.query()
        #print("fff", te._data['char_infos'][0])

        #print("te len:", len(ddd))
        #for aa in te._data['char_infos']:
        #    print("te:", aa['character_width'], end = " " )

    def _textout(self):
        self.gc.change(foreground = self.screen.black_pixel)
        self.window.draw_text(self.gc, self.border,
                    self.te.font_ascent + self.border, self.text)

    def pevent(self, e):
        #print("in button event:", e)
        got = 0
        if e.type == Xlib.X.CreateNotify:
            #self.width = e.width
            #self.height = e.height
            got = True

        if e.type == Xlib.X.EnterNotify:
            attr = self.window.get_attributes()
            self.window.change_attributes(background_pixel=self.lgray)
            ggg=self.window.get_geometry()
            #self.window.clear_area(0, 0, ggg.width, ggg.height)
            self.gc.change(line_width=self.border)
            self.gc.change(foreground = self.ddgray)
            #self.window.rectangle(self.gc, 0, 0, ggg.width-1, ggg.height-1)
            self._textout();
            self.invalidate(self.window)
            got = True

        if e.type == Xlib.X.LeaveNotify:
            self.window.change_attributes(background_pixel=self.dgray)
            ggg=self.window.get_geometry()
            #self.window.clear_area(0, 0, ggg.width, ggg.height)
            self.gc.change(foreground = self.screen.black_pixel)
            self._textout();
            self.invalidate(self.window)
            got = True

        if e.type == Xlib.X.KeyPress:
            print("butt keypress", e)
            got = True

        if e.type == Xlib.X.KeyRelease:
            print("butt keyrelease", e)
            got = True

        return got

# A drawed objects, consisting of either a single
# rhomboid, or two rhomboids connected by a winding line

class Movement(object):
    def __init__(self, win, ev):
        self.win = win

        self.left = ev.event_x - 5
        self.right = ev.event_x + 5
        self.top = ev.event_y - 5
        self.bottom = ev.event_y + 5

        self.time = ev.time
        self.lines = [(ev.event_x, ev.event_y)]

        self.first = Rhomboid(self.win, ev)
        self.last = None

    def motion(self, ev):
        # Find all the mouse coordinates since the
        # last event received

        events = self.win.window.get_motion_events(self.time, ev.time)
        self.time = ev.time

        # Record the previous last coordinate, and append
        # the new coordinates
        firstline = len(self.lines) - 1

        if events:
            # Discard the first coordinate if that is identical to
            # the last recorded coordinate

            pos = events[0]
            if (pos.x, pos.y) == self.lines[-1]:
                events = events[1:]

            # Append all coordinates
            for pos in events:
                x = pos.x
                y = pos.y

                if x < self.left:
                    self.left = x
                if x > self.right:
                    self.right = x

                if y < self.top:
                    self.top = y
                if y > self.bottom:
                    self.bottom = y

                self.lines.append((x, y))

        # Append the event coordinate, if that is different from the
        # last movement coordinate
        if (ev.event_x, ev.event_y) != self.lines[-1]:
            self.lines.append((ev.event_x, ev.event_y))

        # Draw a line between the new coordinates
        self.win.window.poly_line(self.win.gc,
                                  Xlib.X.CoordModeOrigin,
                                  self.lines[firstline:])
    def finish(self, ev):
        self.motion(ev)
        if len(self.lines) > 1:
            self.last = Rhomboid(self.win, ev)

            self.left = min(ev.event_x - 5, self.left)
            self.right = max(ev.event_x + 5, self.right)
            self.top = min(ev.event_y - 5, self.top)
            self.bottom = max(ev.event_y + 5, self.bottom)

    def expose(self, ev):

        # We should check if this object is in the exposed
        # area, but I can't be bothered right now, so just
        # redraw on the last Expose in every batch

        print("Expose:", ev)
        if ev.count == 0:
            self.first.draw()
            if self.last:
                # Redraw all the lines
                self.win.window.poly_line(self.win.gc,
                                          Xlib.X.CoordModeOrigin,
                                          self.lines)
                self.last.draw()

class Rhomboid(object):
    def __init__(self, win, ev):
        self.win = win
        self.x = ev.event_x
        self.y = ev.event_y
        self.draw()

    def draw(self):
        #print("Draw")
        # Draw the segments of the rhomboid
        self.win.window.poly_line(self.win.gc, Xlib.X.CoordModePrevious,
                                  [(self.x, self.y - 5),
                                   (5, 5),
                                   (-5, 5),
                                   (-5, -5),
                                   (5, -5)])

