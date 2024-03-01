import time
import RPi.GPIO as GPIO
from .Utils import chunk
from .Constants import spi, A0, RESN

def display(image: list, config=None) -> None:
    GPIO.output(A0, 0)
    data_slice = chunk(image)
    spi.xfer([0xAF]) # activates the display (0xAE to turn it off)
    for p in range(8):
        GPIO.output(A0, 0)
        spi.xfer([0xB0+p, 0x02, 0x10]) # initializes the column address
        GPIO.output(A0, 1)
        spi.xfer(data_slice[p]) # transfers 1 slice of 128x8 pixels

def reset():
    GPIO.output(RESN, 0)
    time.sleep(0.1)
    GPIO.output(RESN, 1)
    time.sleep(0.1)