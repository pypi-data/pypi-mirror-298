from setuptools import setup, find_packages

setup(
    name="neth",
    version="0.3",
    description="Python library for advanced network scanning, hidden SSID discovery, and Wi-Fi cracking",
    author="Majhool2M",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'scapy',
        'requests',
        'pywifi',
        'opencv-python',
        'netifaces',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
