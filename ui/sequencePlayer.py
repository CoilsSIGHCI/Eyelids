import os
import cv2
import re
import numpy as np
from display.Transmit import display

class SequencePlayer:
    def __init__(self, path, dim=(64, 128)):
        self.path = path
        self.files = self.__files__()
        self.dim = dim

        image0 = cv2.imread(path)
        self.height, self.width = image0.shape[:2]

        self.match  = True
        if self.dim[0] != self.height or self.dim[1] != self.width:
            self.match = False

        self.squash = False
        if len(image0.shape) == 3:
            self.squash = True

    def __files__(self):
        files = os.listdir(self.path)
        files = list(filter(lambda file: re.match(r".*\d+.*", file) and file.endswith(".png"), files))

        def sort_files(file):
            return int(re.findall(r"\d+", file)[0])

        files.sort(key=sort_files)
        return files

    def play(self):
        for file in self.files:
            image = cv2.imread(f"{self.path}/{file}")
            if not self.match:
                image = cv2.resize(image, self.dim)
            if self.squash:
                image = np.mean(image, axis=2).astype(np.uint8)
            display(image)
        print(f"Playing {self.path}")


if __name__ == "__main__":
    player = SequencePlayer(input("Enter the path: "))
    player.play()
