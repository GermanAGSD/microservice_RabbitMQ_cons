import re
import subprocess

def get_ip() -> str:
    out = subprocess.check_output("ipconfig", shell=True, text=True, encoding="cp866", errors="ignore")

    ips = re.findall(r"IPv4-адрес[.\s]*:\s*([0-9.]+)", out)
    print(ips)          # например: ['192.168.3.2']
    print(ips[0])       # первый IP
    return ips[0]