from functools import reduce
from PIL import ImageFont, ImageDraw, Image

# split a string in half. Returns the string if it fits in the image, or calls itself recursively if not
def splitText(text, font, image):
    textWidth = font.getsize(text)[0]
    if textWidth > image.width:
        words = text.split()
        if len(words) == 1:
            return text
        iBeforeMiddle = (len(words) // 2) - 1
        firstHalf = " ".join(words[:iBeforeMiddle + 1])
        index = len(firstHalf)
        secondHalf = text[index + 1:]
        a = splitText(firstHalf, font, image)
        b = splitText(secondHalf, font, image)
        return a + "\n" + b
    else:
        return text
# draw text on image
def draw(filename, text):
    # if first letter is "-", dran text in the bottom of image
    drawOnBottom = text[0] == "-"
    if drawOnBottom:
        text = text[1:].strip()
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("impact.otf", size=(image.height // 10))
    # split to separate lines
    text = splitText(text, font, image)
    black = (0, 0, 0)

    #center text
    x = (image.width // 2) - (font.getsize(text)[0] // 2)

    # set y to 4% of image height
    y = image.height // 25
    if drawOnBottom:
        # set y to 4% from bottom instead of from top
        y = image.height - y - font.getsize(text)[1]
    #draw black border
    draw.text((x-2, y-2), text, font=font, fill=black)
    draw.text((x+2, y-2), text, font=font, fill=black)
    draw.text((x-2, y+2), text, font=font, fill=black)
    draw.text((x+2, y+2), text, font=font, fill=black)

    white = (255, 255, 255)
    draw.text((x, y), text, fill=white, font=font)
    image.save(filename)
    return filename
