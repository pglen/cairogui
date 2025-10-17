


from Xlib.display import Display
from Xlib import X

# 1. Open a connection to the X server
display = Display()

# 2. Load a font
# You can specify a font name that exists on your X server
# For example, "fixed" or "7x14"
font_name = "fixed"
try:
    font = display.open_font(font_name)
except X.BadFont:
    print(f"Error: Font '{font_name}' not found.")
    display.close()
    exit()

# 3. Query font properties
# The font object itself contains attributes corresponding to XFontStruct members
# These include min_bounds, max_bounds, font_ascent, font_descent, etc.
#print(f"Font properties for '{font_name}':")
print(f"  Min Bounds: {font.min_bounds.width}x{font.min_bounds.height}")
print(f"  Max Bounds: {font.max_bounds.width}x{font.max_bounds.height}")
print(f"  Font Ascent: {font.font_ascent}")
print(f"  Font Descent: {font.font_descent}")
print(f"  All Chars Exist: {font.all_chars_exist}")

# You can also access specific properties listed in X11/Xatom.h
# For example, the FONT property itself (which is the font name)
# Note: XGetFontProperty in C takes an atom for the property.
# In python-xlib, many common properties are directly accessible as attributes.

# 4. Close the font and display connection
font.close()
display.close()
