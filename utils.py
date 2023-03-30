
from PIL import Image
def resize_image(Path : str, filename: str):
    sizes = [{
        "width": 1280,
        "height": 720
    }, {
        "width": 640,
        "height": 480
    }]

    for size in sizes:
        size_defined = size['width'], size['height']

        image = Image.open(Path + filename, mode="r")
        image.thumbnail(size_defined)
        image.save(Path + str(size['height']) + "_" + filename)
    print("success")