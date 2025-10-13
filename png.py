from Xlib import display, X  #, Xutil
from PIL import Image, ImageDraw
import os

def render_png(image_path, width, height, x=50, y=50):

    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    image_data = img.tobytes("raw", "RGB")

    disp = display.Display()
    screen = disp.screen()
    root = screen.root

    visual = screen.root_visual  # no exists `default_visual`
    depth = screen.root_depth

    win = root.create_window(
        x, y,
        width, height,
        1,
        depth,
        X.InputOutput,
        visual,
        background_pixel=screen.white_pixel,
        event_mask=X.ExposureMask | X.KeyPressMask | X.StructureNotifyMask
    )

    ximage = X.XCreateImage(disp, visual, depth, 2, 0, image_data, 16, 16, 8, 0)

    win.set_wm_name("PNG image")
    win.map()

    gc = win.create_gc(
        foreground=screen.black_pixel,
        background=screen.white_pixel
    )

    while True:
        event = disp.next_event()
        if event.type == X.Expose:
            if event.count == 0:
                #win.put_pil_image(gc, 0, 0, image_data)
                #win.put_pil_image(gc, 0, 0, img)
                X.XPutImage(disp, win, gc, ximage, 0, 0, 0, 0, 16, 16)

                disp.flush()
        elif event.type == X.KeyPress:
            break
        elif event.type == X.ConfigureNotify:
            pass

    win.destroy()
    disp.close()

if __name__ == '__main__':
    dummy = "dummy.png"

    if not os.path.exists(dummy):
        img = Image.new('RGB', (16, 16), color = 'red')
        d = ImageDraw.Draw(img)
        d.text((1,1), "abc", fill=(255,255,255))
        img.save(dummy)

    render_png(dummy, 200, 200, 100, 100)
