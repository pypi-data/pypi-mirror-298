import cv2
import netifaces
from onvif import ONVIFCamera
import requests
import subprocess


def get_local_ips():
    """جلب جميع عناوين IP المحلية في الشبكة."""
    ips = []
    for interface in netifaces.interfaces():
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for link in addresses[netifaces.AF_INET]:
                ips.append(link['addr'])
    return ips


def discover_cameras_onvif():
    """اكتشاف الكاميرات التي تدعم ONVIF في الشبكة."""
    cameras = []
    ips = get_local_ips()
    
    for ip in ips:
        # نقوم بإنشاء قناة اتصال على بروتوكول ONVIF لاختبار الكاميرات
        try:
            camera = ONVIFCamera(ip, 80, 'admin', 'admin')  # قد تحتاج لتعديل الاسم المستخدم وكلمة المرور
            cameras.append(ip)
        except:
            pass
    return cameras


def discover_cameras_rtsp():
    """اكتشاف الكاميرات التي تدعم RTSP في الشبكة."""
    ips = get_local_ips()
    rtsp_cameras = []
    for ip in ips:
        rtsp_url = f"rtsp://{ip}:554/stream"
        try:
            cap = cv2.VideoCapture(rtsp_url)
            if cap.isOpened():
                rtsp_cameras.append(ip)
                cap.release()
        except:
            pass
    return rtsp_cameras


def access_camera(ip_address, rtsp_port=554):
    """الوصول إلى كاميرا معينة عبر بروتوكول RTSP."""
    rtsp_url = f'rtsp://{ip_address}:{rtsp_port}/stream'
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        print("Failed to access camera.")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Camera Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


def manual_camera_access(ip_address):
    """الدخول إلى كاميرا عن طريق إدخال الـ IP يدويًا."""
    access_camera(ip_address)


def generate_rtsp_link(ip_address):
    """إنشاء رابط RTSP لمشاهدة الكاميرا."""
    rtsp_url = f"rtsp://{ip_address}:554/stream"
    print(f"RTSP Link: {rtsp_url}")
    return rtsp_url


def list_all_cameras():
    """قائمة بجميع الكاميرات المكتشفة (ONVIF و RTSP)."""
    print("Discovering ONVIF cameras...")
    onvif_cameras = discover_cameras_onvif()
    print(f"ONVIF Cameras found: {onvif_cameras}")
    
    print("Discovering RTSP cameras...")
    rtsp_cameras = discover_cameras_rtsp()
    print(f"RTSP Cameras found: {rtsp_cameras}")
    
    all_cameras = onvif_cameras + rtsp_cameras
    return all_cameras