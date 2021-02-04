from PIL import Image

def resize(filePath):
    """Resize the image in filePath to telegram sticker size"""
    image = Image.open(filePath)
    image.thumbnail((512,512))
    newPath = filePath.split('.')[0] + '_r.png'
    image.save(newPath)
    return newPath
