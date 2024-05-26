gesture_direction_group = {
    "upward": [4, 57, 69, 79, 63],
    "downward": [3, 58, 70, 80, 64],
    "leftward": [2, 59, 71, 81, 66, 77],
    "rightward": [1, 60, 72, 82, 65, 78],
    "forward": [5, 68, 83],
    "backward": [6, 67],
    "rotational_clockwise": [10, 14],
    "rotational_counterclockwise": [11, 15],
    "zoom_in": [8, 12],
    "zoom_out": [9, 13],
    "non_directional": [
        7, 16, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
        37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
        55, 56, 61, 62, 74, 75, 76, 73
    ]
}


def get_gesture_direction(gesture: int) -> str:
    for key, value in gesture_direction_group.items():
        if gesture in value:
            return key
    return "non_directional"
