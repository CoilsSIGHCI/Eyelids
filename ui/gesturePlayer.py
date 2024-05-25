from display.Transmit import display


def displayGesture(gesture, radius=16, filled_frame=1, empty_frame=1):
    # create a blinking circle at gesture[x] gesture[y] with r, and fill it with 1, outside the circle with 0
    empty_image = [[0 for _ in range(128)] for _ in range(64)]
    image = empty_image.copy()

    # create a blinking circle
    for frame in range(filled_frame):
        for i in range(64):
            for j in range(128):
                if (i - gesture['y']) ** 2 + (j - gesture['x']) ** 2 < (radius + radius * frame // filled_frame) ** 2:
                    image[i][j] = 1
        display(image)
    for frame in range(empty_frame):
        display(empty_image)
