import NetworkManager as nm

class Network:

    def wlan_ip(self):
        for dev in self.devices():
            if dev.DeviceType is nm.NM_DEVICE_TYPE_WIFI:
                return dev.Ip4Address

    def eth_ip(self):
        for dev in self.devices():
            if dev.DeviceType is nm.NM_DEVICE_TYPE_ETHERNET:
                return dev.Ip4Address

    def devices(self):
        return nm.NetworkManager.GetDevices()

