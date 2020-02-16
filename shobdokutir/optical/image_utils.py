from PIL import Image, ImageChops

def trim_image(img: Image) -> Image:
    """
    Trims the blank spaces from an image.
    Note: It assumes the (0,0) location of the image is a blank space
    """
    bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    else:
        return None