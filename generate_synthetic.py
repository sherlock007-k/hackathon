import pandas as pd
import random

vendors = [
    "HikVision", "TP-Link", "Amazon Echo", "Mi Home", "Bosch Security",
    "Philips Hue", "Sonoff", "Samsung SmartThings", "Unknown Vendor"
]

synthetic = []

for i in range(20):   # create 20 fake devices
    vendor = random.choice(vendors)
    
    # generate random ports (simulate vulnerabilities)
    all_ports = [21,22,23,80,443,8080,8000,2323]
    ports = random.sample(all_ports, random.randint(1,5))
    risk = len([p for p in ports if p in [21,23,2323,80,8080]]) * 20
    risk = min(risk,100)
    
    if risk >= 70: status="High Risk"
    elif risk >=40: status="Medium Risk"
    else: status="Low Risk"

    synthetic.append([
        f"192.168.100.{i+10}",
        vendor,
        len(ports),
        str(ports),
        risk,
        status,
        status  # ml_prediction placeholder
    ])

df = pd.DataFrame(synthetic, columns=[
    "ip","vendor","ports_count","ports","risk_score","status","ml_prediction"
])

df.to_csv("synthetic_data.csv",index=False)
print("Synthetic dataset created!")
