from display.Transmit import display


def displayIdle():
    # create a breathing circle, and fill it with 0, outside the circle with 1
    image = [[0 for _ in range(128)] for _ in range(64)]

    # create a breathing circle
    for frame in range(64):
        for i in range(64):
            for j in range(128):
                if (i - 32) ** 2 + (j - 64) ** 2 < (16 + 16 * frame // 64) ** 2:
                    image[i][j] = 1
        display(image)
