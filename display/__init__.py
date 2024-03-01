import time
import spidev
import RPi.GPIO as GPIO
from .Constants import *

# GPIO initialization
GPIO.setmode(GPIO.BOARD)
GPIO.setup(A0, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RESN, GPIO.OUT, initial=GPIO.HIGH)

# SPI interface initialization
spi.open(0, 0) # bus = 0, device = 0
spi.max_speed_hz = 1000000 # defines the transfer speed (7629 to 125000000)
spi.mode = 0b00 # defines the sequencing of the data and clock pins
# spi.bits_per_word = 8

# application of a reset pulse to the sh1106 circuit
GPIO.output(RESN, 0)
time.sleep(0.1)
GPIO.output(RESN, 1)
time.sleep(0.1)
