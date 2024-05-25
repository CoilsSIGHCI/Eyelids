def testGATT():
    from .GATTService import test
    test()

def start():
    from .GATTService import main
    main()


BLEServiceBaseUrl = "EyelidsConnector"
BLUEZ_SERVICE_NAME = "org.bluez"
GATT_MANAGER_IFACE = "org.bluez.GattManager1"
LE_ADVERTISEMENT_IFACE = "org.bluez.LEAdvertisement1"
LE_ADVERTISING_MANAGER_IFACE = "org.bluez.LEAdvertisingManager1"
AGENT_PATH = "/com/punchthrough/agent"

MainLoop = None

try:
    from gi.repository import GLib

    MainLoop = GLib.MainLoop
except ImportError:
    import gobject as GObject

    MainLoop = GObject.MainLoop

import logging
from .log import logger, logHandler, filelogHandler, formatter

logger.setLevel(logging.DEBUG)
logHandler.setFormatter(formatter)
filelogHandler.setFormatter(formatter)
logger.addHandler(filelogHandler)
logger.addHandler(logHandler)

mainloop = None
bus = None
adapter = None
