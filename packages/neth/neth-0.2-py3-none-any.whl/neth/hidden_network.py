import subprocess

def reveal_hidden_networks():
    # استخدام airodump-ng لكشف الشبكات المخفية
    command = "airodump-ng wlan0mon --showack"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, _ = process.communicate()

    # تحليل النتيجة لإظهار اسم الشبكة المخفية
    networks = []
    for line in output.decode().split('\n'):
        if "Hidden" in line:
            networks.append(line)
    
    return networks