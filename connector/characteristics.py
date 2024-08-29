import array
import json
import os

import globalState
from connector.utils import StrobeState
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
    uuid = "4116F8D2-9F66-4F58-A53D-FC7440E7C14E"
    description = b"GET SET ANIMATION PLAYING ON SCREEN"

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["encrypt-read", "encrypt-write"], service,
        )

        if globalState.get_patterns() is None:
            logger.warning("Patterns not initialized when creating AnimationControl")
        self.add_descriptor(CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        printing_pattern = StrobeState.off
        if globalState.get_patterns() is not None:
            if len(globalState.get_patterns()) > 0:
                printing_pattern = globalState.get_patterns()[0]

        return printing_pattern.value.encode("utf-8")

    def WriteValue(self, value, options):
        logger.debug("Animation Write(raw): " + repr(value))
        decoded_value = bytearray(value).decode("utf-8")
        logger.debug("Animation Write: " + decoded_value)

        logger.debug(f"Playing {decoded_value} animation")
        globalState.set_patterns(globalState.get_patterns() + [StrobeState(decoded_value)])
        # path = self.animation_paths[decoded_value]
        # SequencePlayer(path).play()


class GestureControlCharacteristic(Characteristic):
    uuid = "49B0478D-C1B0-4255-BB55-1FD182638BBB"
    description = b"READ-ONLY HAND GESTURE CONTROL STATUS"

    def __init__(self, bus, index, service):
        Characteristic.__init__(
            self, bus, index, self.uuid, ["encrypt-read"], service,
        )

        if globalState.get_gestures() is None:
            logger.warning("Gestures not initialized when creating GestureControlCharacteristic")

        self.add_descriptor(CharacteristicUserDescriptionDescriptor(bus, 1, self))

    def ReadValue(self, options):
        ges = globalState.get_gestures()
        print(f"Gesture read: {ges[-1]}")
        return bytes(str(ges[-1].__repr__()).replace("'", "\""), "utf-8")


class AutoOffCharacteristic(Characteristic):
    uuid = "9C7DBCE8-DE5F-4168-89DD-74F04F4E5842"
    description = b"Get set auto-off time in minutes"

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
