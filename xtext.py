#!/usr/bin/python3

import sys
sys.path.append("python_xlib")

from Xlib import X, display
import time
import argparse
from datetime import datetime

def main():
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Display text using X11')
    parser.add_argument('--text', help='Text to display')
    parser.add_argument('--fg-color', default='white',
                       help='Text color (white/black or hex color like #FFBB00)')
    parser.add_argument('--bg-color', default='black',
                       help='Background color (white/black or hex color like #000000)')
    parser.add_argument('--delay', type=int, default=3,
                       help='Display for n seconds')
    parser.add_argument('--font', type=str,
                       default='-misc-fixed-medium-r-normal--13-120-75-75-c-70-iso8859-1',
                       help='X11 font name')
    args = parser.parse_args()

    #Update text to show current time if no text argument provided
    #print(args.text)
    if not args.text:
        current_time = datetime.now().strftime('%H:%M:%S')
        text = current_time.encode()
    else:
        text = args.text.encode()

    # Connect to the X server
    # Connect to the X server
    disp = display.Display()
    screen = disp.screen()
    root = screen.root

    # Load font first to calculate text dimensions
    try:
        font = disp.open_font(args.font)
        print(f"Successfully loaded font", dir(font))
    except Exception as e:
        #print(f"Error loading font: {e}")
        return

    # Calculate text dimensions before creating window

    text_extents = font.query_text_extents(text)
    text_width = text_extents.overall_width
    text_height = text_extents.font_ascent + text_extents.font_descent

    print(f"Successfully loaded font", text, text_extents)

    # Add padding to the window size
    padding_x = 20  # 10px padding on each side
    padding_y = 20  # 10px padding on top and bottom
    width = text_width + padding_x
    height = text_height + padding_y

    # Calculate position for top right corner
    screen_width = screen.width_in_pixels
    x_pos = screen_width - width - 10
    y_pos = 10

    # Create window with calculated dimensions
    win = root.create_window(
        x_pos, y_pos, width, height, 0,
        screen.root_depth,
        X.InputOutput,
        X.CopyFromParent,
        override_redirect=True
    )

    # Set window type to remove borders
    win.change_property(
        disp.intern_atom("_NET_WM_WINDOW_TYPE"),
        disp.intern_atom("ATOM"), 32,
        [disp.intern_atom("_NET_WM_WINDOW_TYPE_DIALOG")]
    )

    win.map()

    def parse_color(color_str):
        if color_str.lower() == 'white':
            return disp.screen().white_pixel
        elif color_str.lower() == 'black':
            return disp.screen().black_pixel
        elif color_str.startswith('#'):
            # Convert hex color to RGB values
            r = int(color_str[1:3], 16) << 16
            g = int(color_str[3:5], 16) << 8
            b = int(color_str[5:7], 16)
            return r | g | b
        return disp.screen().black_pixel

    fg_pixel = parse_color(args.fg_color)
    bg_pixel = parse_color(args.bg_color)

    gc = win.create_gc(
        foreground=fg_pixel,
        background=bg_pixel,
        #font = font.id
    )

    #gc.font = font.id
    #gc.font = font

    #Get text dimensions
    text_extents = font.query_text_extents(text)
    text_width = text_extents.overall_width
    text_height = text_extents.font_ascent + text_extents.font_descent

    # Update text position calculation
    x = padding_x // 2  # Center horizontally with padding
    y = (height + text_height) // 2  # Center vertically

    win.change_attributes(background_pixel=bg_pixel)
    win.clear_area(0, 0, width, height)

    # Draw text at calculated center position
    #win.poly_text(gc, x, y, [(0, text)])
    win.poly_text(gc, x, y, [text])

    # Flush changes
    disp.flush()
    disp.sync()

    # Keep the window open for 5 seconds
    try:
        time.sleep(args.delay)
    finally:
        win.destroy()

if __name__ == "__main__":
    main()
    print("Done")

