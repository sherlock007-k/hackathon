# scanner.py
import scapy.all as scapy
import socket
from vendor import get_vendor   # to fetch vendor details

# ------------------ Network Scanner ------------------
def scan_network(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    answered = scapy.srp(broadcast/arp_request, timeout=2, verbose=False)[0]

    devices = []
    for send, receive in answered:
        devices.append({
            "ip": receive.psrc,
            "mac": receive.hwsrc,
            "vendor": get_vendor(receive.hwsrc)
        })
    return devices

# ------------------ Port Scanner ------------------
def scan_ports(ip, ports=[21,22,23,80,443,8080,2323]):
    open_ports = []
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.4)
            if s.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            s.close()
        except:
            pass
    return open_ports

# ------------------ Device Risk Analyzer ------------------
def analyze_device(ip, mac):
    vendor = get_vendor(mac)
    open_ports = scan_ports(ip)

    # BASE RISK SCORING
    risk = 0
    if any(p in open_ports for p in [21,23,2323]): risk += 40
    if any(p in open_ports for p in [80,8080]): risk += 25
    if any(p in open_ports for p in [22,443]): risk += 5

    if vendor=="Unknown Vendor": risk+=20
    if "CCTV" in vendor.upper(): risk+=30
    if "ESP" in vendor.upper(): risk+=20

    risk = min(risk,100)

    label = (
        "High" if risk>60 else
        "Medium" if risk>25 else
        "Low"
    )

    return {
        "ip":ip,
        "mac":mac,
        "vendor":vendor,
        "open_ports":open_ports,
        "ports_count":len(open_ports),
        "risk_score":risk,
        "risk_label":label
    }


if __name__=="__main__":
    print("\nScanning...")
    d=scan_network("192.168.1.0/24")
    for dev in d:
        print(analyze_device(dev['ip'],dev['mac']))
