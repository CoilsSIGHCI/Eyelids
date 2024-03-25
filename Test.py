from time import sleep

from ui.sequencePlayer import SequencePlayer
from hw import is_raspberry_pi
import os
from mvp.predict import Model

model = Model()

if __name__ == "__main__":
    if is_raspberry_pi():
        path = os.path.expanduser("~/EyelidsSequences/test")
    else:
        path = input("Enter the path: ")
    player = SequencePlayer(path)
    player.play()
    print("Done")