"""
Display all visible SSIDs
"""
import NetworkManager as nm
import dbus
from log import logger


class Network(object):

    def __init__(self):
        self.SERVER_SSID = "czesc_piekna"
        self.searchAP()
        is_connected = self.isConnected()
        if is_connected != True:
            connection = self.getConnection()
            if connection is not False:
                self.connect(connection)
            else:
                logger.warning("Network: Connection is not added")
            self.isConnected()

    def searchAP(self):
        for dev in nm.NetworkManager.GetDevices():
            if dev.DeviceType != nm.NM_DEVICE_TYPE_WIFI:
                continue
            for ap in dev.GetAccessPoints():
                if (ap.Ssid == self.SERVER_SSID):
                    logger.info('Network: Found server access point: %s %dMHz %d%%',
                                ap.Ssid, ap.Frequency, ap.Strength)

    def isConnected(self):
        for connection in nm.NetworkManager.ActiveConnections:
            connection_id = connection.Connection.GetSettings()['connection']['id']
            if connection_id == self.SERVER_SSID:
                logger.info("Network: Connected")
                return True
        logger.warning("Network: Not connected")
        return False

    def getConnection(self):
        connections = nm.Settings.ListConnections()
        for connection in connections:
            connection_id = connection.GetSettings()['connection']['id']
            if connection_id == self.SERVER_SSID:
                logger.info("Network: Found connection %s", connection_id)
                return connection
        logger.info("Network: Can't find connection %s", self.SERVER_SSID)
        return False

    def connect(self, connection):
        if not nm.NetworkManager.NetworkingEnabled:
            nm.NetworkManager.Enable(True)
        logger.info("Network: Connecting...")
        connection_type = connection.GetSettings()['connection']['type']
        devices = nm.NetworkManager.GetDevices()
        for dev in devices:
            if dev.DeviceType == nm.NM_DEVICE_TYPE_WIFI:
                logger.info("Network: Activating connection...")
                try:
                    nm.NetworkManager.ActivateConnection(connection, dev, "/")
                except dbus.exceptions.DBusException as e:
                    logger.error("Network: Error: %s", e)
