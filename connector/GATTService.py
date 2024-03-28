import dbus
import dbus.exceptions
import dbus.mainloop.glib
import dbus.service

from connector import BLUEZ_SERVICE_NAME, GATT_MANAGER_IFACE, LE_ADVERTISING_MANAGER_IFACE, AGENT_PATH, MainLoop
from .ble import (
    Advertisement,
    Service,
    Application,
    find_adapter,
    Agent,
)
from .characteristics import AnimationControl, GestureControlCharacteristic, AutoOffCharacteristic
from .log import logger
from .utils import register_app_cb, register_app_error_cb, register_ad_cb, register_ad_error_cb


class EyelidsConnectorService(Service):
    SVC_UUID = "D57D86F6-E6F3-4BE4-A3D1-A71119D27AD3"

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.SVC_UUID, True)
        self.add_characteristic(AnimationControl(bus, 0, self))
        self.add_characteristic(GestureControlCharacteristic(bus, 1, self))
        self.add_characteristic(AutoOffCharacteristic(bus, 2, self))


class ServiceAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, "peripheral")
        self.add_manufacturer_data(
            # pseudo manufacturer data
            0xFFFF, [0x70, 0x74],
        )
        self.add_service_uuid(EyelidsConnectorService.SVC_UUID)

        self.add_local_name("Eyelids")
        print(self.GetAll("org.bluez.LEAdvertisement1"))
        self.include_tx_power = True


def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    # get the system bus
    bus = dbus.SystemBus()
    # get the ble controller
    adapter = find_adapter(bus)

    if not adapter:
        logger.critical("GattManager1 interface not found")
        return

    adapter_obj = bus.get_object(BLUEZ_SERVICE_NAME, adapter)

    adapter_props = dbus.Interface(adapter_obj, "org.freedesktop.DBus.Properties")

    # powered property on the controller to on
    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    # Get manager objs
    service_manager = dbus.Interface(adapter_obj, GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(adapter_obj, LE_ADVERTISING_MANAGER_IFACE)

    advertisement = ServiceAdvertisement(bus, 0)
    obj = bus.get_object(BLUEZ_SERVICE_NAME, "/org/bluez")

    agent = Agent(bus, AGENT_PATH)

    app = Application(bus)
    app.add_service(EyelidsConnectorService(bus, 1))

    mainloop = MainLoop()

    agent_manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    agent_manager.RegisterAgent(AGENT_PATH, "NoInputNoOutput")

    ad_manager.RegisterAdvertisement(
        advertisement.get_path(),
        {},
        reply_handler=register_ad_cb,
        error_handler=register_ad_error_cb,
    )

    logger.info("Registering GATT application...")

    service_manager.RegisterApplication(
        app.get_path(),
        {},
        reply_handler=register_app_cb,
        error_handler=[register_app_error_cb],
    )

    agent_manager.RequestDefaultAgent(AGENT_PATH)

    mainloop.run()
    # ad_manager.UnregisterAdvertisement(advertisement)
    # dbus.service.Object.remove_from_connection(advertisement)


def test():
    main()


if __name__ == "__main__":
    main()
