import re
import subprocess
import shutil
def get_ip() -> str:
    out = subprocess.check_output("ipconfig", shell=True, text=True, encoding="cp866", errors="ignore")

    ips = re.findall(r"IPv4-адрес[.\s]*:\s*([0-9.]+)", out)
    print(ips)          # например: ['192.168.3.2']
    print(ips[0])       # первый IP
    return ips[0]

def read_memory():

    path = "C:\\"  # диск/папка, для которой считаем место
    total, used, free = shutil.disk_usage(path)

    gb = 1024**3
    print(f"Total: {total/gb:.2f} GB")
    print(f"Used : {used/gb:.2f} GB")
    print(f"Free : {free/gb:.2f} GB")
    return free/gb
