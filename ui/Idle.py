from display.Transmit import display


def displayIdle(duration=64):
    image = [[255 for _ in range(128)] for _ in range(64)]
    radius = 48

    for frame in range(duration):
        for i in range(64):
            for j in range(128):
                if (i - 32) ** 2 + (j - 64) ** 2 < (radius + 16 * frame // duration) ** 2:
                    image[i][j] = 0
        display(image)

    image = [[0 for _ in range(128)] for _ in range(64)]
    for frame in range(duration):
        for i in range(64):
            for j in range(128):
                if (i - 32) ** 2 + (j - 64) ** 2 >= (radius + 16 * (duration - frame) // duration) ** 2:
                    image[i][j] = 255
        display(image)
