#!/usr/bin/python

import sys, time
from Xlib import X, display, Xutil, ext
import Xlib

# Establish a connection to the X server
disp = display.Display()

# Define window dimensions and position
x, y, width, height = 100, 100, 300, 200

event_maskx =  (    X.ExposureMask |
                    X.StructureNotifyMask |
                    X.SubstructureNotifyMask |
                    X.SubstructureRedirectMask |
                    X.ButtonPressMask |
                    X.ButtonReleaseMask |
                    #X.Button1MotionMask |
                    X.PointerMotionMask |
                    X.PointerMotionHintMask |
                    X.KeyPressMask |
                    X.KeyReleaseMask |
                    X.EnterWindowMask |
                    X.LeaveWindowMask |
                    X.ResizeRedirectMask |
                    X.PropertyChangeMask |
                    X.VisibilityChangeMask |
                    X.CWEventMask |
                    X.FocusChangeMask )

class BaseWindow(object):

    def __init__(self, display, parent, xx, yy, www, hhh, border = 0):

        self.d = display
        self.objects = []
        #self.texts = []
        #self.texts.append("Hello")
        self.entered = False
        self.width = 10
        self.height = 10
        self.screen = self.d.screen()

        self.colormap = self.screen.default_colormap
        self.blue  = self.colormap.alloc_color(0x4fff, 0x4fff, 0xffff).pixel
        self.green = self.colormap.alloc_color(0x4fff, 0xffff, 0x4fff).pixel
        self.red = self.colormap.alloc_color(0xffff, 0x4fff, 0x4fff).pixel
        self.gray = self.colormap.alloc_color(0xcfff, 0xcfff, 0xcfff).pixel
        self.lgray = self.colormap.alloc_color(0xdfff, 0xdfff, 0xdfff).pixel
        self.dgray = self.colormap.alloc_color(0xbfff, 0xbfff, 0xbfff).pixel

        #print("lookup", self.colormap.lookup_color("green"))

        # Find which screen to open the window on
        #print("screen", self.screen)

        #self.root = self.screen.root
        #self.HELLO_WORLD = self.d.intern_atom(b'HELLO_WORLD')

        self.window = parent.create_window(
            xx, yy, www, hhh,
            border,
            self.screen.root_depth,
            X.InputOutput,
            X.CopyFromParent,
            background_pixel = self.gray, #screen.white_pixel,
            event_mask = event_maskx,
            colormap = X.CopyFromParent,
            #keys = {'backing_store': X.NotUseful, 'all_event_masks': 1980679760, }
            )

        #print("exts", disp.list_extensions())
        #print("fonts", disp.get_font_path())

        font_name = "fixed-medium"
        font_size = 18
        fontx = "*%s*--%d*" % (font_name, font_size)
        #print("fontx", fontx)
        #self.lll = disp.list_fonts_with_info(fontx, 100)
        self.lll = disp.list_fonts(fontx, 100)
        #for aa in self.lll:
        #    print(aa)
        #XFontStruct *font = XLoadQueryFont(dpy, font_name);
        font = disp.open_font(self.lll[0])
        #print("font:", font)

        self.gc = self.window.create_gc(
            foreground = self.green, # self.screen.black_pixel,
            background = self.green, # self.screen.white_pixel,
            font=font,
            line_width=1,
            line_style=X.LineOnOffDash,
            cap_style=X.CapRound,
            #join_style=X.JoinMiter
            #join_style=X.JoinRound
            join_style=X.JoinBevel
            )
        #self.gc.change(line_width=5)
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
        self.geom = self.window.get_geometry()
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
        #display.flush()

class Window(BaseWindow):

    def __init__(self, display, parent , xx, yy, www, hhh):
        super().__init__(display, parent, xx, yy, www, hhh)
        self.children = []
        child = pButton(self.d, self.window, width//4, height//4, width//2, height//2,
                    border = 0)
        self.children.append(child)
        child.window.map()

    # Main loop, handling events
    def winloop(self):
        current = None
        while 1:
            e = self.d.next_event()
            if e.type == X.ButtonPress:
                if self.d.get_input_focus().focus != e.window:
                    e.window.set_input_focus(X.RevertToParent, X.CurrentTime )
                    print("focus change:", self.d.get_input_focus().focus, "child:", e.window)
            for aa in self.children:
                if e.window == aa.window :
                    ret = aa.pevent(e)
                    #print("ret:", ret)
                    if ret:
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
                        break
                        #sys.exit(0)

            # Window has been destroyed, quit
            if e.type == X.DestroyNotify:
                print("Exit dest")
                break
                #sys.exit(0)

            #continue

            # Some part of the window has been exposed,
            # redraw all the objects.
            if e.type == X.Expose:
                pass
                #if e.count == 0:
                #    self.window.fill_rectangle(self.gc, 0, 0, 60, 60)

                #print("****Expose", e)
                #for oo in self.objects:
                #    oo.expose(e)
                #for tt in self.texts:
                #    print(tt)

            # Left button pressed, start to draw
            if e.type == X.ButtonPress and e.detail == 1:

                current = Movement(self, e)
                self.objects.append(current)
                #self.sendevent()
                self.window.draw_text(self.gc, 100, 100, b"Hello, world!")
                self.window.poly_line(self.gc, X.CoordModeOrigin,
                                [(20, 20), (100, 100), (120, 150)], )
                self.invalidate(self.window)

            # Left button released, finish drawing
            if e.type == X.ButtonRelease and e.detail == 1 and current:
                current.finish(e)
                current = None

            # Mouse movement with button pressed, draw
            if e.type == X.MotionNotify and current:
                current.motion(e)

            if e.type == X.KeyPress:
                print("main keypress", e)

        # Exit
        print("Exited loop.")

class pButton(BaseWindow):

    def __init__(self, display, parent, xx, yy, www, hhh, border = 0):

        super().__init__(display, parent, xx, yy, www, hhh, border)
        self.window.change_attributes(background_pixel=self.dgray)
        ggg=self.window.get_geometry()
        self.window.clear_area(0, 0, ggg.width, ggg.height)
        #self.invalidate(self.window)

    def pevent(self, e):
        #print("in button event:", e)
        got = 0
        if e.type == X.CreateNotify:
            #self.x = e.x
            #self.y = e.y
            self.width = e.width
            self.height = e.height
            got = True

        if e.type == X.EnterNotify:
            attr = self.window.get_attributes()
            self.window.change_attributes(background_pixel=self.lgray)
            ggg=self.window.get_geometry()
            self.window.clear_area(0, 0, ggg.width, ggg.height)
            self.invalidate(self.window)
            got = True

        if e.type == X.LeaveNotify:
            self.window.change_attributes(background_pixel=self.dgray)
            ggg=self.window.get_geometry()
            self.window.clear_area(0, 0, ggg.width, ggg.height)
            self.invalidate(self.window)
            got = True

        if e.type == X.KeyPress:
            print("butt keypress", e)
            got = True
        if e.type == X.KeyRelease:
            print("butt keypress", e)
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
                                  X.CoordModeOrigin,
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
                                          X.CoordModeOrigin,
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
        self.win.window.poly_line(self.win.gc, X.CoordModePrevious,
                                  [(self.x, self.y - 5),
                                   (5, 5),
                                   (-5, 5),
                                   (-5, -5),
                                   (5, -5)])
win = Window(disp, disp.screen().root, x, y, width, height)
win.winloop()

# Close the display connection
disp.close()

# EOF
