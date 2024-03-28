import logging

logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
filelogHandler = logging.FileHandler("/tmp/ble_gatt.log")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
