import array
import json
import os
from enum import Enum

import dbus
import dbus.service

from connector.ble import GATT_CHRC_IFACE, DBUS_PROP_IFACE, logger, Descriptor
from connector.exceptions import NotPermittedException, InvalidArgsException, NotSupportedException
from connector.log import logger
from ui.sequencePlayer import SequencePlayer


class Characteristic(dbus.service.Object):
    """
    org.bluez.GattCharacteristic1 interface implementation
    """

    def __init__(self, bus, index, uuid, flags, service):
        self.path = service.path + "/char" + str(index)
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
            GATT_CHRC_IFACE: {
                "Service": self.service.get_path(),
                "UUID": self.uuid,
                "Flags": self.flags,
                "Descriptors": dbus.Array(self.get_descriptor_paths(), signature="o"),
            }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_descriptor(self, descriptor):
        self.descriptors.append(descriptor)

    def get_descriptor_paths(self):
        result = []
        for desc in self.descriptors:
            result.append(desc.get_path())
        return result

    def get_descriptors(self):
        return self.descriptors

    @dbus.service.method(DBUS_PROP_IFACE, in_signature="s", out_signature="a{sv}")
    def GetAll(self, interface):
        if interface != GATT_CHRC_IFACE:
            raise InvalidArgsException()

        return self.get_properties()[GATT_CHRC_IFACE]

    @dbus.service.method(GATT_CHRC_IFACE, in_signature="a{sv}", out_signature="ay")
    def ReadValue(self, options):
        logger.info("Default ReadValue called, returning error")
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE, in_signature="aya{sv}")
    def WriteValue(self, value, options):
        logger.info("Default WriteValue called, returning error")
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StartNotify(self):
        logger.info("Default StartNotify called, returning error")
        raise NotSupportedException()

    @dbus.service.method(GATT_CHRC_IFACE)
    def StopNotify(self):
        logger.info("Default StopNotify called, returning error")
        raise NotSupportedException()

    @dbus.service.signal(DBUS_PROP_IFACE, signature="sa{sv}as")
    def PropertiesChanged(self, interface, changed, invalidated):
        pass


class AnimationControl(Characteristic):
    uuid = "4116f8d2-9f66-4f58-a53d-fc7440e7c14e"
    description = b"Get\x14set\x14animation\x14playing\x14on\x14screen"


    class State(Enum):
        strobe = "STROBE"
        off = "OFF"
        slideRight = "SLIDE_RIGHT"

        @classmethod
        def has_value(cls, value):
            return value in cls._value2member_map_


    animation_paths = {
        State.strobe.value: os.path.expanduser("~/EyelidsSequences/Strobe"),
        State.slideRight.value: os.path.expanduser("~/EyelidsSequences/HMove"),
    }

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["encrypt-read", "encrypt-write"], service,
        )

        self.value = self.State.off
        self.add_descriptor(CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        logger.debug("Animation Read: " + repr(self.value))

        return self.value.value.encode("utf-8")

    def WriteValue(self, value, options):
        decoded_value = bytearray(value).decode("utf-8")
        logger.debug("Animation Write(raw): " + repr(value))
        logger.debug("Animation Write: " + decoded_value)

        if not self.State.has_value(decoded_value):
            logger.error("Invalid value: " + repr(value))
            return
        if decoded_value == self.State.off.value:
            logger.debug("There should be a interrupt function here, but it is not implemented yet.")
        else:
            self.value = decoded_value
            logger.debug(f"Playing {decoded_value} animation")
            path = self.animation_paths[decoded_value]
            SequencePlayer(path).play()

        logger.debug("Animation ended ")
        self.value = self.State.off


class GestureControlCharacteristic(Characteristic):
    uuid = "49B0478D-C1B0-4255-BB55-1FD182638BBB"
    description = b"Read-only\x14hand\x14gesture\x14control\x14status"

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["encrypt-read"], service,
        )

        self.value = {"x": 0, "y": 0, "gesture": "UNKNOWN"}
        self.add_descriptor(CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        logger.info("boiler read: " + repr(self.value))
        encoded = json.encoder.JSONEncoder().encode(self.value)
        return bytes(encoded, "utf-8")


class AutoOffCharacteristic(Characteristic):
    uuid = "9c7dbce8-de5f-4168-89dd-74f04f4e5842"
    description = b"Get/set autoff time in minutes"

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["secure-read", "secure-write"], service,
        )

        self.value = []
        self.add_descriptor(CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        logger.info("auto off read: " + repr(self.value))

        return self.value

    def WriteValue(self, value, options):
        logger.info("auto off write: " + repr(value))
        cmd = bytes(value)

        # write it to machine
        logger.info(f"writing {cmd} to machine")


class CharacteristicUserDescriptionDescriptor(Descriptor):
    """
    Writable CUD descriptor.
    """

    CUD_UUID = "2901"

    def __init__(
            self, bus, index, characteristic,
    ):
        self.value = array.array("B", characteristic.description)
        self.value = self.value.tolist()
        Descriptor.__init__(self, bus, index, self.CUD_UUID, ["read"], characteristic)

    def ReadValue(self, options):
        return self.value

    def WriteValue(self, value, options):
        if not self.writable:
            raise NotPermittedException()
        self.value = value
