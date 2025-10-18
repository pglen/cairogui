from Xlib import X, display

# Open the display
disp = display.Display()
screen = disp.screen()
root_window = screen.root

# Define window parameters
x, y, width, height = 100, 100, 400, 300
border_width = 0  # No border

# Create a window attributes object
attrs = X.CWOverrideRedirect | X.CWBackPixel
#attr_mask = X.SetWindowAttributes()
#attr_mask.override_redirect = True  # Crucial for removing decorations
#attr_mask.background_pixel = screen.white_pixel

# Create the window
window = root_window.create_window(
    x, y, width, height, border_width,
    screen.root_depth,
    X.InputOutput,
    X.CopyFromParent,
    attrs,
    #attr_mask
)

# Select input events (optional, but useful for user interaction)
window.change_attributes(event_mask=X.ExposureMask | X.KeyPressMask)
window.change_attributes(override_redirect=True)

# Map the window (make it visible)
window.map() #_raised()

# Event loop (to keep the window open and handle events)
while True:
    event = disp.next_event()
    if event.type == X.KeyPress:
        # Handle key presses (e.g., exit on a specific key)
        print("Key pressed!")
        break
    elif event.type == X.Expose:
        # Handle expose events (e.g., redraw window content)
        print("Window exposed!")

# Close the display
disp.close()
