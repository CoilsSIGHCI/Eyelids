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


def displayNavigation(command: StrobeState, duration=128):
    directions = [StrobeState.navForward, StrobeState.navBackward, StrobeState.navLeft, StrobeState.navRight]
    directionMap = {
        StrobeState.navForward: "upward",
        StrobeState.navBackward: "downward",
        StrobeState.navLeft: "leftward",
        StrobeState.navRight: "rightward",
    }

    if directions.__contains__(command):
        displayGesture(directionMap[command], shape='circle', duration=duration)
    else:
        SequencePlayer(animation_paths["STROBE"]).play()
