def Crop(url):
    from io import BytesIO
    from random import randint

    import requests
    from PIL import Image

    r = requests.get(url)
    im = Image.open(BytesIO(r.content))

    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size

    # Setting the points for cropped image
    left = randint(0, int(width * 0.7))
    top = randint(0, int(height * 0.7))

    right = left + int(width * 0.3)
    bottom = top + int(height * 0.3)

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))

    im1 = im1.save("file.png")