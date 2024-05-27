import os
from time import sleep

import cv2
import re
import numpy as np

from connector.utils import StrobeState
from display.Transmit import display

animation_paths = {
    StrobeState.strobe.value: os.path.expanduser("~/Eyelids/seq/Strobe"),
    StrobeState.slideRight.value: os.path.expanduser("~/Eyelids/seq/HMove-R"),
    StrobeState.slideLeft.value: os.path.expanduser("~/Eyelids/seq/HMove"),
}

class SequencePlayer:
    def __init__(self, path, dim=(64, 128)):
        self.path = path
        self.files = self.__files__()
        self.dim = dim

        image0 = cv2.imread(self.files[0])
        self.height, self.width = image0.shape[:2]

        self.match  = True
        if self.dim[0] != self.height or self.dim[1] != self.width:
            self.match = False

        self.squash = False
        if len(image0.shape) == 3:
            self.squash = True

        # check if alpha channel is present
        if len(image0.shape) == 3 and image0.shape[2] == 4:
            self.alpha = True

        print(f"match: {self.match}, squash: {self.squash}, alpha: {image0.shape}")

    def __files__(self):
        files = os.listdir(self.path)
        files = list(filter(lambda file: re.match(r".*\d+.*", file) and file.endswith(".png"), files))

        def sort_files(file):
            return int(re.findall(r"\d+", file)[0])

        files.sort(key=sort_files)
        files = list(map(lambda file: f"{self.path}/{file}", files))
        return files

    def __play_single__(self, file):
        image = cv2.imread(file)
        if not self.match:
            image = cv2.resize(image, self.dim)
        if self.squash:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        display(image.tolist())

    def play(self):
        print(f"Playing {self.path}")
        for file in self.files:
            self.__play_single__(file)


if __name__ == "__main__":
    player = SequencePlayer(input("Enter the path: "))
    player.play()
