import spidev


A0 = 22 # GPIO pin for A0 pin: 0 -> command; 1 -> display data RAM
RESN = 18 # GPIO pin for display reset (active low)
spi = spidev.SpiDev()
