# center_text.py

from PIL import Image, ImageDraw, ImageFont

fontx = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
text = "Pillow Rocks!"

def center(output_path):
    #width, height = (400, 400)
    font = ImageFont.truetype(fontx, size=24)
    font_width, font_height = font.getsize(text)
    image = Image.new("RGB", (font_width, font_height), "grey")
    draw = ImageDraw.Draw(image)

    #new_width = (width - font_width) / 2
    #new_height = (height - font_height) / 2
    draw.text((0, 0), text, fill="black", font=font)
    image.save(output_path)

if __name__ == "__main__":
    center("centered_text.jpg")
