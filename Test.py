import os

import connector
from hw import is_raspberry_pi
from mvp.Options import PresetOptionsResNetL
from mvp.predict import GestureService, MODEL_PATH, MODEL_TYPE
from ui.sequencePlayer import SequencePlayer

# model = GestureService(opt=PresetOptionsResNetL(model=MODEL_TYPE, width_mult=1, pretrain_path=MODEL_PATH))

if __name__ == "__main__":
    test_item = input("test: ")
    if test_item == "seq":
        if is_raspberry_pi():
            path = os.path.expanduser("~/EyelidsSequences/test")
        else:
            path = input("Enter the path: ")
        player = SequencePlayer(path)
        player.play()
        print("Done")
    elif test_item == "predict":
        # model.test()
        pass
    elif test_item == "gatt":
        connector.testGATT()
    else:
        print("Invalid test item")
