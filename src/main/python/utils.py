from PIL import Image, ImageCms

def limit_scale(image, width, height):
    if image.width > width or image.height > height:
        if image.width/image.height > width/height:
            scale_size = (width, width * image.height//image.width)
        else:
            scale_size = (height * image.width//image.height, height)

        return image.resize(scale_size)
    else:
        return image