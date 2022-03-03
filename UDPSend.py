#
# This file is part of the F3FChrono distribution (https://github.com/jomarin38/F3FChrono).
# Copyright (c) 2021 Sylvain DAVIET, Joel MARIN.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import socket
import time
import logging
import sys
from PyQt5.QtCore import QObject


INITMSG = "Init"
EVENTMSG = "Event"

class udpsend(QObject):
    def __init__(self, udpip, udpport):
        super(QObject, self).__init__()
        self.udpip = udpip
        self.port = udpport
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def __del__(self):
        del self.sock

    def send(self):
        self.sock.sendto(bytes('event', 'utf-8'), (self.udpip, self.port))

    def sendData(self, data):
        self.sock.sendto(bytes(data, 'utf-8'), (self.udpip, self.port))
        print (data)

    def terminate(self):
        print('terminated event')
        self.sock.sendto(bytes('terminated', 'utf-8'), (self.udpip, self.port))


class find_ip():
    def __init__(self):
        print("init")

    def get_ip(self):
        import itertools
        import os
        import re


        ip = []
        broadcast = []
        f = os.popen('ifconfig')
        for iface in [' '.join(i) for i in
                      iter(lambda: list(itertools.takewhile(lambda l: not l.isspace(), f)), [])]:
            int = re.findall('^(eth?|wlan?|enp?|wlps?)[0-9]', iface)
            if int and re.findall('RUNNING', iface):
                ip.append(re.findall(r'(?<=inet\s)[\d.-]+', iface)[0])
                broadcast.append(re.findall(r'(?<=broadcast\s)[\d.-]+', iface)[0])
        return ip, broadcast

if __name__ == '__main__':
    print ("UDP Beep Debug")
    #udpbeep = udpBeep ("192.168.0.22", 4445)
    print(find_ip().get_ip())
    '''
    udpBeep = udpbeep ("255.255.255.255", 4445)
    end=False

    while not end:
        cmdline=sys.stdin.readline ()
        print (cmdline)
        if (cmdline=="terminate\n"):
            udpBeep.terminate()
            end = True
        else:
            udpBeep.send()
   '''
