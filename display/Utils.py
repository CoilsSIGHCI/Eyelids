from PIL import Image


def chunk(image: list, config=None) -> list:
    data_slice = [[], [], [], [], [], [], [], []]
    for p in range(0, 8):  # the image is divided into 8 horizontal slices of 8 pixels
        data_set = []
        for c in range(0, 128):  # each slice is 8x128 px
            by = 0x00
            for b in range(0, 8):
                by = by >> 1 | image[p * 8 + b][c] & 0x80
            data_set.append(by)
        data_slice[p] = data_set

    return data_slice


def get_image_data_list(image: Image, band=None) -> list:
    flat_pixel = list(image.getdata(band))

    # flip up side down
    flat_pixel.reverse()
    image_data = []
    for y in range(image.height):
        image_data.append(flat_pixel[y * image.width:(y + 1) * image.width])

    return image_data
