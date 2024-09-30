import pywifi
from pywifi import const

def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    scan_results = iface.scan_results()

    networks = []
    for network in scan_results:
        networks.append({
            'ssid': network.ssid if network.ssid else 'Hidden Network',
            'bssid': network.bssid,
            'signal': network.signal,
            'auth': network.auth,
            'akm': network.akm,
        })
    return networks