__author__ = 'AlexM'
import subprocess
import re
import sys
import os
import socket

from scr import DSEARCH_PATH

# ####some routines to find local ip (from http://stackoverflow.com/questions/11735821/python-get-localhost-ip)
if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                                                            ifname[:15]))[20:24])


def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
        ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


LATRONIX_TYPE = "X9"  # type of XPort device (to reduce results) it can be X5!!!


def get_asb9_ip(result_as_str=True):
    """find latronix device and return it IP
     :returns list of IP's """
    try:
        localhost = get_lan_ip()
        if not os.path.isfile(DSEARCH_PATH):
            raise RuntimeError("dsearch.exe is not found!")
        # res = subprocess.check_output([DSEARCH_PATH, localhost, LATRONIX_TYPE])
        res = subprocess.check_output([DSEARCH_PATH, localhost])
        ip = re.findall(r'(?P<ip>[0-9]+(?:\.[0-9]+){3})', res, re.MULTILINE)
        print ip

    except (RuntimeError,) as e:
        print e
        sys.exit()
    else:
        if not ip or len(ip) > 3:
            raise Exception("wrong account of devices")
        if localhost in ip:
            ip.remove(localhost)
        if ip:
            ip = ip.pop() if result_as_str else ip
            return res, ip
        else:
            raise Exception("Device not found(maybe it ready) or something goes wrong")