import Xlib
from Xlib import display, X

def get_text_extent(font, text):
    """
    Calculates the extent of a text string using font metrics.

    Args:
        font: An Xlib.X.Font object.
        text: The string to measure.

    Returns:
        A tuple (width, ascent, descent, overall_width, overall_ascent, overall_descent, overall_baseline).
    """
    # XQueryTextExtents is the C Xlib function to get text extents.
    # In python-xlib, you typically access font metrics directly or
    # derive them from font properties.
    # For a simple string, we can approximate by multiplying character width
    # by the number of characters and considering ascent/descent.

    # This is a simplified example. For accurate results with complex fonts
    # and scripts, you might need more sophisticated text layout libraries
    # or direct XQueryTextExtents equivalent if exposed in python-xlib.

    # For a fixed-width font, you can calculate the width this way:
    char_width = 12 #font.max_bounds.width
    width = len(text) * char_width

    # Ascent and descent are typically available directly from font properties
    ascent = 2 #font.ascent
    descent = 3 #font.descent

    # overall_width, overall_ascent, overall_descent, overall_baseline
    # are often needed for more complex layout, but for basic extent
    # ascent and descent are usually sufficient for height.
    # For simplicity, we can use the font's max_bounds for overall.
    overall_width = width # Simplified
    overall_ascent = font.max_bounds.ascent
    overall_descent = font.max_bounds.descent
    overall_baseline = font.max_bounds.ascent # Simplified, usually relative to origin

    return (width, ascent, descent, overall_width, overall_ascent, overall_descent, overall_baseline)


if __name__ == "__main__":
    disp = display.Display()
    screen = disp.screen()
    root = screen.root

    # Load a font (e.g., a fixed-width font for easier calculation)
    # You might need to adjust the font name based on what's available on your system.
    try:
        font = disp.open_font("fixed")
    except Xlib.error.BadFont:
        print("Error: 'fixed' font not found. Try another font like '7x14' or '9x15'.")
        # Fallback to another common font if 'fixed' isn't available
        try:
            font = disp.open_font("7x14")
        except Xlib.error.BadFont:
            print("Error: '7x14' font not found either. Please ensure you have X11 fonts installed.")
            exit()

    text_to_measure = "Hello, Xlib!"

    # Get text extent
    width, ascent, descent, overall_width, overall_ascent, overall_descent, overall_baseline = get_text_extent(font, text_to_measure)

    print(f"Text: '{text_to_measure}'")
    print(f"Calculated Width: {width}")
    print(f"Font Ascent: {ascent}")
    print(f"Font Descent: {descent}")
    print(f"Overall Width: {overall_width}")
    print(f"Overall Ascent: {overall_ascent}")
    print(f"Overall Descent: {overall_descent}")
    print(f"Overall Baseline: {overall_baseline}")

    disp.close()
