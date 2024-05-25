from realtime.run import run
import threading

def start_realtime(callback, capture_device: int = 0, playback: bool = False):
    t = threading.Thread(target=run, args=(callback, capture_device, playback))
    t.start()
    return t
