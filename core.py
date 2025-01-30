import os
import sys
import subprocess

modules = ["pyzipper", "rarfile", "tkinter", "threading", "webbrowser"]

def install_module(module):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        print(f"{module} başarıyla yüklendi!")
    except Exception as e:
        print(f"{module} yüklenirken hata oluştu: {e}")

def check_and_install():
    for module in modules:
        try:
            __import__(module)
            print(f"{module} zaten yüklü.")
        except ImportError:
            print(f"{module} bulunamadı, yükleniyor...")
            install_module(module)

    if os.name != "nt":  # Sadece Linux için
        try:
            subprocess.check_call(["sudo", "apt", "install", "-y", "unrar"])
            print("unrar başarıyla yüklendi!")
        except Exception as e:
            print(f"unrar yüklenirken hata oluştu: {e}")

if __name__ == "__main__":
    check_and_install()
