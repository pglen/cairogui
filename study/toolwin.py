import Xlib
from Xlib import display, X, Xatom
from Xlib.protocol import event
from Xlib.error import XError

def create_tool_window(disp, screen, x, y, width, height):
    """Creates a window and sets its type to _NET_WM_WINDOW_TYPE_TOOL."""

    # Get the root window
    root = screen.root

    # Create the window
    window = root.create_window(
        x, y, width, height, 0,
        screen.root_depth,
        X.InputOutput,
        X.CopyFromParent,
        background_pixel=screen.white_pixel,
        event_mask=X.ExposureMask | X.StructureNotifyMask | X.KeyPressMask
    )

    #_NET_WM_WINDOW_TYPE_DESKTOP, ATOM
    #_NET_WM_WINDOW_TYPE_DOCK, ATOM
    #_NET_WM_WINDOW_TYPE_TOOLBAR, ATOM
    #_NET_WM_WINDOW_TYPE_MENU, ATOM
    #_NET_WM_WINDOW_TYPE_UTILITY, ATOM
    #_NET_WM_WINDOW_TYPE_SPLASH, ATOM
    #_NET_WM_WINDOW_TYPE_DIALOG, ATOM
    #_NET_WM_WINDOW_TYPE_NORMAL, ATOM

    # Atom for _NET_WM_WINDOW_TYPE and _NET_WM_WINDOW_TYPE_XXX
    net_wm_window_type = disp.intern_atom('_NET_WM_WINDOW_TYPE')
    net_wm_window_type_tool = disp.intern_atom('_NET_WM_WINDOW_TYPE_TOOL')
    net_wm_window_type_toolbar = disp.intern_atom('_NET_WM_WINDOW_TYPE_TOOLBAR')
    net_wm_window_type_utility = disp.intern_atom('_NET_WM_WINDOW_TYPE_UTILITY')
    net_wm_window_type_dock = disp.intern_atom('_NET_WM_WINDOW_TYPE_DOCK')
    net_wm_window_type_dialog = disp.intern_atom('_NET_WM_WINDOW_TYPE_DIALOG')
    net_wm_window_type_normal = disp.intern_atom('_NET_WM_WINDOW_TYPE_NORMAL')
    #net_wm_window_type_menu = disp.intern_atom('_NET_WM_WINDOW_TYPE_MENU')
    net_wm_window_type_menu = disp.intern_atom('_NET_WM_WINDOW_TYPE_POPUP_MENU')
    net_wm_window_type_notify = disp.intern_atom('_NET_WM_WINDOW_TYPE_NOTIFICATION')

    # Set the _NET_WM_WINDOW_TYPE property
    #window.change_property(
    #    net_wm_window_type,
    #    Xatom.ATOM,
    #    #X.A_ATOM,  # Property type is ATOM
    #    32,        # Format is 32-bit
    #    [net_wm_window_type_menu]
    #)

    #net_motif_state = disp.intern_atom('_MOTIF_WM_HINTS')

    net_wm_window_actions = disp.intern_atom('_NET_WM_ALLOWED_ACTIONS')
    #net_wm_action_move _NET_WM_ACTION_MOVE, ATOM
    net_wm_action_close = disp.intern_atom('_NET_WM_ACTION_CLOSE')

    #_NET_WM_ACTION_RESIZE, _NET_WM_ACTION_RESIZE, _NET_WM_ACTION_RESIZE, ATOM
    #_NET_WM_ACTION_MINIMIZE, ATOM
    #_NET_WM_ACTION_SHADE, ATOM
    #_NET_WM_ACTION_STICK, ATOM
    #_NET_WM_ACTION_MAXIMIZE_HORZ, ATOM
    #_NET_WM_ACTION_MAXIMIZE_VERT, ATOM
    #_NET_WM_ACTION_FULLSCREEN, ATOM
    #_NET_WM_ACTION_CHANGE_DESKTOP, ATOM
    #net_wm_action_resize = disp.intern_atom('_NET_WM_ACTION_RESIZE')
    #net_wm_action_close  = disp.intern_atom('_NET_WM_ACTION_CLOSE')

    #window.change_property(
    #    net_wm_window_actions,
    #    Xatom.ATOM,
    #    #X.A_ATOM,  # Property type is ATOM
    #    32,        # Format is 32-bit
    #    [net_wm_action_close]
    #)

    net_wm_state = disp.intern_atom('_NET_WM_STATE')
    net_wm_shaded = disp.intern_atom('_NET_WM_STATE_SHADED')
    net_wm_sticky = disp.intern_atom('_NET_WM_STATE_STICKY')

    motif_wm_hints = disp.intern_atom('_MOTIF_WM_HINTS')
    mwm_decor_all = disp.intern_atom('MWM_INPUT_MODELESS')

    window.change_property(
        motif_wm_hints,
        Xatom.ATOM,
        #X.A_ATOM,  # Property type is ATOM
        32,        # Format is 32-bit
        [mwm_decor_all]
    )

    #window.change_property(
    #    net_wm_state,
    #    Xatom.ATOM,
    #    #X.A_ATOM,  # Property type is ATOM
    #    32,        # Format is 32-bit
    #    [net_wm_sticky]
    #)

    #window.change_attributes(override_redirect=True)

    def getatom (atom):
        return disp.intern_atom(atom)

    data = [getatom("_NET_WM_ACTION_ABOVE"),getatom("_NET_WM_ACTION_CLOSE"),
        getatom("_NET_WM_ACTION_BELOW"),getatom("_NET_WM_ACTION_CHANGE_DESKTOP"),
        getatom("_NET_WM_ACTION_SHADE")]
    state = getatom("_NET_WM_ALLOWED_ACTIONS")
    event = Xlib.protocol.event.ClientMessage(window = window,
                            client_type = state, data = (32, data))
    root.send_event(event, X.SubstructureRedirectMask)

    #disp.flush()
    #disp.sync()

    # Set the window title
    #window.set_wm_name("My Tool Window")

    # Map the window to make it visible
    window.map()


    return window

if __name__ == '__main__':
    # Connect to the X server
    disp = display.Display()
    screen = disp.screen()

    # Create the tool window
    tool_win = create_tool_window(disp, screen, 100, 100, 200, 150)

    # Event loop
    while True:
        try:
            e = disp.next_event()
            if e.type == X.KeyPress:
                # Exit on any key press
                break
            elif e.type == X.Expose:
                # Redraw content if needed (for demonstration, not drawing anything here)
                pass
        except XError as err:
            print(f"X Error: {err}")
            break

    # Unmap and destroy the window
    tool_win.unmap()
    tool_win.destroy()
    disp.close()
