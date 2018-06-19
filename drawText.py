from PIL import ImageFont, ImageDraw, Image

def draw(filename, text):
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("impact.otf", size=128)
    draw.text((10, 10), text, fill=(255, 255, 255), font=font)
    image.save(filename)
    return filename
