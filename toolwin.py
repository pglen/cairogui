#!/usr/bin/python

import Xlib.display
from Xlib import X, Xatom

def set_motif_hints(disp, win):

    # Define constants for MWM_HINTS
    MWM_HINTS_DECORATIONS = (1 << 1)
    MWM_DECOR_NONE = 0

    class MwmHints:
        def __init__(self, flags=0, functions=0, decorations=0, input_mode=0, status=0):
            self.flags = flags
            self.functions = functions
            self.decorations = decorations
            self.input_mode = input_mode
            self.status = status

    # Set the _MOTIF_WM_HINTS property to remove decorations
    wm_hints_atom = disp.intern_atom("_MOTIF_WM_HINTS")
    mwm_hints = MwmHints(flags=MWM_HINTS_DECORATIONS, decorations=MWM_DECOR_NONE)

    # Pack the MwmHints struct into bytes for Xlib
    # This assumes a 32-bit system where unsigned long is 4 bytes
    # For 64-bit systems, unsigned long might be 8 bytes, requiring adjustment
    data = (mwm_hints.flags, mwm_hints.functions, mwm_hints.decorations,
            mwm_hints.input_mode, mwm_hints.status)

    # The type of the property is usually MWM_HINTS_DECORATIONS (an atom)
    # The format is 32 (meaning each element in data is a 32-bit long)
    win.change_property(wm_hints_atom, wm_hints_atom, 32, data)

    net_wm_window_type = disp.intern_atom('_NET_WM_WINDOW_TYPE')
    net_wm_window_type_tool = disp.intern_atom('_NET_WM_WINDOW_TYPE_TOOL')
    net_wm_window_type_toolbar = disp.intern_atom('_NET_WM_WINDOW_TYPE_TOOLBAR')

    win.change_property(
        net_wm_window_type,
        Xatom.ATOM,
        32,        # Format is 32-bit
        [net_wm_window_type_toolbar]
    )

def create_borderless_window():
    disp = Xlib.display.Display()
    screen = disp.screen()
    root = screen.root

    # Create a simple window
    win = root.create_window(
        0, 0, 400, 300, 0,
        screen.root_depth,
        X.InputOutput,
        X.CopyFromParent,
        background_pixel=screen.white_pixel,
        event_mask=X.ExposureMask | X.StructureNotifyMask | X.KeyPressMask
    )
    set_motif_hints(disp, win)
    win.map()
    #display.sync()

    # Event loop to keep the window open
    while True:
        event = disp.next_event()
        if event.type == X.Expose:
            # Handle redraws if necessary
            pass
        if event.type == X.KeyPress:
            # Exit on any key press
            break

if __name__ == "__main__":
    create_borderless_window()
