from enum import Enum

from connector import mainloop
from .log import logger


def register_app_cb():
    logger.info("GATT application registered")


def register_app_error_cb(error):
    logger.critical("Failed to register application: " + str(error))
    mainloop.quit()


def register_ad_cb():
    logger.info("Advertisement registered")


def register_ad_error_cb(error):
    logger.critical("Failed to register advertisement: " + str(error))
    mainloop.quit()


class StrobeState(Enum):
    strobe = "STROBE"
    off = "OFF"
    slideRight = "SLIDE_RIGHT"
    slideLeft = "SLIDE_LEFT"
    glow = "GLOW"
    navForward = "NAV_FORWARD"
    navBackward = "NAV_BACKWARD"
    navLeft = "NAV_LEFT"
    navRight = "NAV_RIGHT"
    navStop = "NAV_STOP"

    @staticmethod
    def isNavigable(value: Enum) -> bool:
        return str(value.value).startswith("NAV_")

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
