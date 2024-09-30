# لا نقوم باستيراد الوحدات في بداية الملف لتجنب الاستيراد الدائري

def scan_wifi():
    from .wifi_scanner import scan_wifi as _scan_wifi
    return _scan_wifi()

def reveal_hidden_networks():
    from .hidden_network import reveal_hidden_networks as _reveal_hidden_networks
    return _reveal_hidden_networks()

def crack_wifi(network_bssid, wordlist_path, interface='wlan0'):
    from .wifi_cracker import crack_wifi as _crack_wifi
    return _crack_wifi(network_bssid, wordlist_path, interface)

def get_network_info(ip_range):
    from .network_info import get_network_info as _get_network_info
    return _get_network_info(ip_range)

def access_camera(ip_address, rtsp_port=554):
    from .camera_hacking import access_camera as _access_camera
    return _access_camera(ip_address, rtsp_port)

def manual_camera_access(ip_address):
    from .camera_hacking import manual_camera_access as _manual_camera_access
    return _manual_camera_access(ip_address)

def generate_rtsp_link(ip_address):
    from .camera_hacking import generate_rtsp_link as _generate_rtsp_link
    return _generate_rtsp_link(ip_address)

def list_all_cameras():
    from .camera_hacking import list_all_cameras as _list_all_cameras
    return _list_all_cameras()
