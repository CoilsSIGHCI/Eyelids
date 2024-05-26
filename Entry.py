import os
import threading
import connector
from connector.utils import StrobeState
from hw import is_raspberry_pi
from ui.sequencePlayer import SequencePlayer, animation_paths
from ui.gesturePlayer import displayGesture
from ui.Idle import displayIdle
from mvp.wrapper import start_realtime, start_gatt

import globalState


class EyelidsDevice:
    @staticmethod
    def updateGesture(gesture):
        if gesture is not None:
            globalState.set_gestures([gesture])
        else:
            globalState.set_gestures([])

    @staticmethod
    def startGATT():
        start_gatt()

    @staticmethod
    def startRealtime():
        start_realtime(EyelidsDevice.updateGesture, playback=False)

    def loop(self):
        while True:
            if len(globalState.get_gestures()) > 0:
                gesture = globalState.get_gestures()[0]
                if gesture is not None and len(globalState.get_gestures()) > 0:
                    displayGesture(gesture)
                    globalState.set_gestures(globalState.get_gestures()[1:])
            elif len(globalState.get_patterns()) > 0:
                pattern = globalState.get_patterns()[0]
                SequencePlayer(animation_paths[pattern]).play()
                globalState.set_patterns(globalState.get_patterns()[1:])
            else:
                displayIdle()

    def __init__(self):
        EyelidsDevice.startGATT()
        # EyelidsDevice.startRealtime()
        self.loop()


if __name__ == "__main__":
    # sequence = SequencePlayer(animation_paths[StrobeState.strobe.value])
    # sequence.play()
    eyelids = EyelidsDevice()
