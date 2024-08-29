from connector.utils import StrobeState
from display.Transmit import display
from ui.sequencePlayer import SequencePlayer, animation_paths


def displayGesture(gesture, shape='circle', radius=16, duration=128):
    empty_image = [[0 for _ in range(128)] for _ in range(64)]

    # Ease-out curve
    def ease_out(t):
        return 1 - (1 - t) ** 2

    for frame in range(duration):
        image = empty_image.copy()
        progress = ease_out(frame / duration)

        for i in range(64):
            for j in range(128):
                if shape == 'circle':
                    if (i - gesture["y"]) ** 2 + (j - gesture["x"]) ** 2 < (radius + 16 * progress) ** 2:
                        image[i][j] = 255
                elif shape == 'stride':
                    if gesture["direction"] in ["upward", "downward"]:
                        if abs(j - gesture["x"]) < radius and abs(i - gesture["y"] - 32 * progress * (
                                1 if gesture["direction"] == "downward" else -1)) < radius:
                            image[i][j] = 255
                    else:  # leftward or rightward
                        if abs(i - gesture["y"]) < radius and abs(j - gesture["x"] - 64 * progress * (
                                1 if gesture["direction"] == "rightward" else -1)) < radius:
                            image[i][j] = 255
                elif shape == 'fill':
                    if gesture["direction"] == "upward" and i > 64 - 64 * progress:
                        image[i][j] = 255
                    elif gesture["direction"] == "downward" and i < 64 * progress:
                        image[i][j] = 255
                    elif gesture["direction"] == "leftward" and j > 128 - 128 * progress:
                        image[i][j] = 255
                    elif gesture["direction"] == "rightward" and j < 128 * progress:
                        image[i][j] = 255

        display(image)


def displayNavigation(direction: StrobeState, duration=32):
    width, height = 128, 64
    empty_image = [[0 for _ in range(width)] for _ in range(height)]

    for frame in range(duration):
        image = empty_image.copy()
        progress = frame / duration

        if direction in [StrobeState.navForward, StrobeState.navBackward]:
            stride_width = 64
            stride_height = 16
            start_y = height if direction == StrobeState.navForward else 0
            end_y = 0 if direction == StrobeState.navForward else height
            current_y = int(start_y + (end_y - start_y) * progress)

            for i in range(height):
                for j in range(width):
                    if abs(j - width // 2) < stride_width // 2 and abs(i - current_y) < stride_height // 2:
                        image[height - 1 - i][width - 1 - j] = 255

        elif direction in [StrobeState.navLeft, StrobeState.navRight]:
            center_y = height // 2
            start_x = width if direction == StrobeState.navLeft else 0
            end_x = 0 if direction == StrobeState.navLeft else width
            current_x = int(start_x + (end_x - start_x) * progress)
            radius = 16

            for i in range(height):
                for j in range(width):
                    if (i - center_y) ** 2 + (j - current_x) ** 2 <= radius ** 2:
                        image[height - 1 - i][width - 1 - j] = 255

        elif direction == StrobeState.navStop:
            center_x, center_y = width // 2, height // 2
            radius = int(min(width, height) * 0.4 * progress)
            for i in range(height):
                for j in range(width):
                    if (i - center_y) ** 2 + (j - center_x) ** 2 <= radius ** 2:
                        image[height - 1 - i][width - 1 - j] = 255

        display(image)
