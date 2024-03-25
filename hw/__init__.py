import os
import platform


def is_raspberry_pi():
    """Checks if the platform is a Raspberry Pi."""
    command = "cat /proc/cpuinfo | grep Model"
    returnString = os.popen(command).read()
    return all([
        'aarch64' in platform.uname().machine,
        returnString.find("Raspberry") != -1
    ])
