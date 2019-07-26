__author__ = 'AlexM'
import telnetlib
from time import sleep
import socket
import logging
import sys

DEFAULT_IP = "0.0.0.0"
DEFAULT_TELNET_PORT = 9999
DEFAULT_TIMEOUT = 2
SAVE_EXIT = '9'

logger = logging.getLogger('asb_setup')


class ASB9Telnet(telnetlib.Telnet, object):
    Baudrate = '38400'
    I_F_Mode = '4C'
    Flow = '00'
    ConnectMode = 'CC'
    Datagram_Type = '01'
    Broadcast = 'Y'
    Pack_Cntrl = '20'
    SendChar_1 = 'FF'
    SendChar_2 = 'FF'

    def __init__(self, host, port, new_ip, new_port):
        try:
            super(ASB9Telnet, self).__init__(host, port)
            self.new_ip = new_ip
            self.new_port = new_port
            # self.tn = telnetlib.Telnet(host,port)
            # self.tn.set_debuglevel(9)
        except socket.error:
            logging.info("Can't connect to ASB9, check if where is another active session!")
            sys.exit(-1)

    def start_session(self):
        self.read_until("Press Enter for Setup Mode")
        self.send_enter()

    def send_enter(self):
        # self.tn.write(""+"\n\r")
        self.write(b"\r")

    def wait(self, n=1):
        sleep(n)

    def get_octet(self, n=0):
        if self.new_ip:
            return self.new_ip.split('.')[n]

    def set_ip(self):
        try:
            logging.info("Start IP setup...")
            self.read_until("Your choice ?")
            self.write("0".encode('ascii') + b"\r")
            self.wait()
            # ###setup IP
            self.read_until("*", timeout=DEFAULT_TIMEOUT)
            self.write(self.get_octet(0).encode('ascii') + b"\r")
            self.wait()
            self.read_until("*", timeout=DEFAULT_TIMEOUT)
            self.write(self.get_octet(1).encode('ascii') + b"\r")
            self.wait()
            self.read_until("*", timeout=DEFAULT_TIMEOUT)
            self.write(self.get_octet(2).encode('ascii') + b"\r")
            self.wait()
            self.read_until("*", timeout=DEFAULT_TIMEOUT)
            self.write(self.get_octet(3).encode('ascii') + b"\r")
            self.wait()
            # ###

            self.read_until("Set Gateway IP Address (N) ?", timeout=DEFAULT_TIMEOUT)
            self.wait()
            self.send_enter()

            self.read_until("Netmask: Number of Bits for Host Part (0=default) (0)", timeout=DEFAULT_TIMEOUT)
            self.write("16".encode('ascii') + b"\r")

            self.read_until("Set DNS Server IP addr  (N) ?", timeout=DEFAULT_TIMEOUT)
            self.wait()
            self.send_enter()

            self.read_until("Change Telnet/Web Manager password (N) ?", timeout=DEFAULT_TIMEOUT)
            self.wait()
            self.send_enter()

            logging.info("IP setup done!")
        except (Exception, ) as e:
            print "Set IP fails {0}".format(e)

    def set_channel1(self):
        try:
            logging.info("Start chanel setup...")
            self.read_until("Your choice ?")
            self.write("1".encode('ascii') + b"\r")
            self.wait()
            # ###setup packet
            self.read_until("Baudrate (9600) ?", timeout=DEFAULT_TIMEOUT)
            self.write(self.Baudrate.encode('ascii') + b"\r")
            self.wait()

            self.read_until("I/F Mode (4C) ?", timeout=DEFAULT_TIMEOUT)
            # self.write(self.I_F_Mode.encode('ascii') + b"\r")
            self.send_enter()
            self.wait()

            self.read_until("Flow (00) ?", timeout=DEFAULT_TIMEOUT)
            #self.write(self.Flow.encode('ascii') + b"\r")
            self.send_enter()
            self.wait()

            self.read_until("Port No", timeout=DEFAULT_TIMEOUT)
            self.write(self.new_port.encode('ascii') + b"\r")
            self.wait()

            self.read_until("ConnectMode", timeout=DEFAULT_TIMEOUT)
            self.write(self.ConnectMode.encode('ascii') + b"\r")
            self.wait()

            self.read_until("Datagram Type", timeout=DEFAULT_TIMEOUT)
            self.write(self.Datagram_Type.encode('ascii') + b"\r")
            self.wait()

            self.read_until("Send as Broadcast", timeout=DEFAULT_TIMEOUT)
            self.write(self.Broadcast.encode('ascii'))
            self.wait()

            self.read_until("Remote Port", timeout=DEFAULT_TIMEOUT)
            self.write(self.new_port.encode('ascii') + b"\r")
            self.wait()

            self.read_until("Pack Cntrl", timeout=DEFAULT_TIMEOUT)
            self.write(self.Pack_Cntrl.encode('ascii') + b"\r")
            self.wait()

            self.read_until("SendChar 1", timeout=DEFAULT_TIMEOUT)
            self.write(self.SendChar_1.encode('ascii') + b"\r")
            self.wait()

            self.read_until("SendChar 2", timeout=DEFAULT_TIMEOUT)
            self.write(self.SendChar_2.encode('ascii') + b"\r")
            self.wait()
        except (Exception, ) as e:
            print "Set Chanell fails {0}".format(e)

            # logger.info("Channel1 setup done!\n")

    def save(self):
        try:
            self.read_until("Your choice ?")
            self.write(SAVE_EXIT.encode('ascii') + b"\r")
            # logger.info("Saving...\n")
        except Exception as e:
            # logger.info("ERROR {0}".format(e))
            print "save fails {0}".format(e)
        finally:
            self.close()


# def parse_arguments():
# parser = argparse.ArgumentParser()
#     parser.add_argument("ip", type=str, help="New Device IP")
#     parser.add_argument("port", type=str, help="Device port")
#     parser.add_argument("-host_ip", type=str, default=DEFAULT_IP,
#                         help="Host IP address\or left it blank for new device")
#
#     args = parser.parse_args()
#     data = {'ip': args.ip, 'port': args.port, 'host_ip': args.host_ip}
#     logging.info(data)
#     return data

