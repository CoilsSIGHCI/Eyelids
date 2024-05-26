from display.Transmit import display
from spatial import get_gesture_direction


def displayGesture(gesture, radius=16, duration=128):
    empty_image = [[0 for _ in range(128)] for _ in range(64)]

    # Ease-out curve
    def ease_out(t):
        return 1 - (1 - t) ** 2

    # Create a circle with radius r, filled with 255, and
    # move it according to the gesture direction
    # (upward, downward, leftward, rightward)

    for frame in range(duration):
        image = empty_image.copy()
        for i in range(64):
            for j in range(128):
                if gesture["direction"] == "upward":
                    if (i - gesture["y"]) ** 2 + (j - gesture["x"]) ** 2 < (radius + 16 * frame // duration) ** 2:
                        image[i][j] = 255
                elif gesture["direction"] == "downward":
                    if (i - gesture["y"]) ** 2 + (j - gesture["x"]) ** 2 < (radius + 16 * frame // duration) ** 2:
                        image[i][j] = 255
                elif gesture["direction"] == "leftward":
                    if (i - gesture["y"]) ** 2 + (j - gesture["x"]) ** 2 < (radius + 16 * frame // duration) ** 2:
                        image[i][j] = 255
                elif gesture["direction"] == "rightward":
                    if (i - gesture["y"]) ** 2 + (j - gesture["x"]) ** 2 < (radius + 16 * frame // duration) ** 2:
                        image[i][j] = 255
        display(image)
