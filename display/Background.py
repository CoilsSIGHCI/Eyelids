import math


def background(density: float):
    if density < 0 or density > 1:
        raise ValueError("Invalid density value. Must be between 0 and 1.")
    if density == 0:
        return [[0 for _ in range(128)] for _ in range(64)]
    if density == 1:
        return [[255 for _ in range(128)] for _ in range(64)]

    h_stride = math.floor(1 / density)
    v_stride = math.ceil(3 ** 0.5 / density / 2)

    image = [[0 for _ in range(128)] for _ in range(64)]

    # odd rows
    for i in range(0, 64, v_stride * 2):
        for j in range(0, 128, h_stride):
            image[i][j] = 255
    for i in range(v_stride, 64, v_stride * 2):
        for j in range(math.floor(h_stride / 2), 128, h_stride):
            image[i][j] = 255

    return image

def glowBackground():
    from .Transmit import display
    for i in range(1, 100):
        display(background(i/100))
    for i in range(100, 0, -1):
        display(background(i/100))