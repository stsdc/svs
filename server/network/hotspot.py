# source https://gist.github.com/terbo/a8d4021af0cb4729133a
import os
import re
import string
import subprocess
import sys
import time

import humanize as pp
from netaddr import *

from log import logger


class HotSpot(object):
    def __init__(self):
        self.HOSTAPD_CONTROL_PATH = '/var/run/hostapd'
        self.HOSTAPD_CLI_PATH = '/usr/sbin/hostapd_cli'
        self.IFCONFIG_PATH = '/sbin/ifconfig'
        self.ARP_PATH = '/usr/sbin/arp'
        self.ARP_FLAGS = '-a'  # n may be added

        self.hostapd_interfaces = os.listdir(self.HOSTAPD_CONTROL_PATH)
        self.hostapd_uptime = 0

        self.clients = dict()
        self.arp_table = dict()
        self.hostapd_stats = dict()

    def get_hostapd(self):
        for hostapd_iface in self.hostapd_interfaces:
            hostapd_cli_cmd = [self.HOSTAPD_CLI_PATH, '-i', hostapd_iface, 'all_sta']
            self.hostapd_uptime = time.time() - int(os.stat('%s/%s' %
                                                            (self.HOSTAPD_CONTROL_PATH, hostapd_iface))[9])

            all_sta_output = subprocess.Popen(
                hostapd_cli_cmd, stdout=subprocess.PIPE).communicate()[0]
            hostapd_output = subprocess.Popen(
                [self.HOSTAPD_CLI_PATH, 'status'], stdout=subprocess.PIPE).communicate()[0].split('\n')

            channel = re.sub('channel=', '', hostapd_output[16])
            bssid = re.sub('bssid\[0\]=', '', hostapd_output[24])
            ssid = re.sub('ssid\[0\]=', '', hostapd_output[25])
            clientcount = int(re.sub('num_sta\[0\]=', '', hostapd_output[26]))

            self.hostapd_stats[hostapd_iface] = [ssid, bssid, channel, clientcount]

            macreg = r'^(' + r'[:-]'.join([r'[0-9a-fA-F]{2}'] * 6) + r')$'
            stas = re.split(macreg, all_sta_output, flags=re.MULTILINE)

            mac = rx = tx = ctime = ''
            for sta_output in stas:

                for line in sta_output.split('\n'):
                    if re.match(macreg, line):
                        mac = line
                    if re.match('rx_packets', line):
                        rx = re.sub('rx_packets=', '', line)
                    if re.match('tx_packets', line):
                        tx = re.sub('tx_packets=', '', line)
                    if re.match('connected_time=', line):
                        ctime = re.sub('connected_time=', '', line)

                if mac and rx and tx and ctime:
                    self.clients[mac] = [ctime, rx, tx]

    def get_arp_table(self):
        arp_output = subprocess.Popen([self.ARP_PATH, self.ARP_FLAGS],
                                      stdout=subprocess.PIPE).communicate()[0].split('\n')

        for line in xrange(len(arp_output)):
            l = arp_output[line].split(' ')
            try:
                iface = l[6]

                if iface in self.hostapd_interfaces:
                    ip = l[1]
                    hostname = l[0]
                    mac = l[3]

                    if re.match('[A-Z0-9][A-Z0-9]:', mac, re.IGNORECASE):
                        if mac in self.clients:
                            self.clients[mac].extend([ip, hostname])
                            self.clients[mac].append(self.get_vendor(mac))
            except:
                pass

    def get_vendor(self, mac):
        try:
            vendor = EUI(mac).oui.registration().org
        except:
            vendor = 'Unknown'
        return vendor

    def check(self):
        self.get_hostapd()
        self.get_arp_table()
        # self.show()
        if self.clients:
            logger.debug("HotSpot: Clients:%s", bool(self.clients))
            for mac in self.clients:
                try:
                    logger.info("HotSpot: Connected client: %s, %s, %s", self.clients[mac][4], self.clients[mac][3],
                                self.clients[mac][5])
                except IndexError as e:
                    logger.error("HotSpot: error: %s", e)
            return True
        else:
            logger.warning("HotSpot: No clients")
        return False

    def show(self):
        print self.clients
        print self.hostapd_stats
