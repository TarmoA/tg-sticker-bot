from PIL import Image

def resize(filePath):
    """Resize the image in filePath to telegram sticker size"""
    image = Image.open(filePath)
    width, height = image.size
    if width < 512 and height < 512:
        bigger = max([width, height])
        if bigger == width:
            height = 512 * height / width
            width = 512
        else:
            width = 512 * width / height
            height = 512
        image = image.resize(width, height)
    image.thumbnail((512,512))
    newPath = filePath.split('.')[0] + '_r.png'
    image.save(newPath)
    return newPath
