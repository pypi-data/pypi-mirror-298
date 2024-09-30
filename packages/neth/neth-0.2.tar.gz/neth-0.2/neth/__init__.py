import neth

# فحص الشبكات المتاحة
networks = neth.scan_wifi()
print(networks)

# كشف الشبكات المخفية
hidden_networks = neth.reveal_hidden_networks()
print(hidden_networks)

# كسر كلمة مرور شبكة معينة
result = neth.crack_wifi('XX:XX:XX:XX:XX:XX', 'wordlist.txt')
print(result)

# الوصول إلى كاميرا معينة
neth.access_camera('192.168.1.101')

# اكتشاف جميع الكاميرات في الشبكة
cameras = neth.list_all_cameras()
print(cameras)
