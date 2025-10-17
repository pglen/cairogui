   #font_name = "fixed*medium*normal"
    ##font_name = "fixed*medium"
    ##font_name = "terminal*medium"
    #font_size = 18
    #fontx = "*%s*--%d*" % (font_name, font_size)
    ##fontx = "*"
    ##print("fontx", fontx)
    ##self.lll = self.d.list_fonts_with_info(fontx, 100)
    #lll = disp.list_fonts(fontx, 10)
    #for aa in lll:
    #    print(aa)
    ##XFontStruct *font = XLoadQueryFont(dpy, font_name);
    #gl_font = disp.open_font(lll[0])
    ##gl_font = disp.open_font("fixed")
    #print("\bfont:", gl_font)
    #gl_font.add_file('action_man_bold.ttf')
 #!/usr/bin/env python3

import Xlib
from Xlib import display, X   # X is also needed

def pperror():
    print("error")

display = Xlib.display.Display()

display.set_error_handler(pperror);

screen = display.screen()
root = screen.root

#print(root.get_attributes())
root.change_attributes(event_mask=X.ExposureMask)  # "adds" this event mask
#print(root.get_attributes())  # see the difference

gc = root.create_gc(foreground = screen.white_pixel, background = screen.black_pixel)

def draw_it():
    root.draw_text(gc, 200, 200, b"Hello, world!")
    display.flush()

draw_it()
while 1:
    if display.pending_events() != 0:  # check to safely apply next_event
        event = display.next_event()
        if event.type == X.Expose and event.count == 0:
            draw_it()
