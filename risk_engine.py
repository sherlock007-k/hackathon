def calculate_risk(ports, vendor):
    risk = 0

    # High risk ports
    for p in [21,23,2323]:
        if p in ports: risk += 40

    # Medium risk ports
    for p in [80,8080,8000]:
        if p in ports: risk += 25

    # Low risk ports
    for p in [443,22]:
        if p in ports: risk += 5

    # Vendor-based trust score
    if vendor in ["Unknown Vendor","Unknown","",None]:
        risk += 20
    if vendor and "CCTV" in vendor.upper(): risk += 30
    if vendor and "ESP" in vendor.upper(): risk += 20

    return min(risk,100)   # cap to 100

# Test risk function
if __name__ == "__main__":
    print("Test:", calculate_risk([23,80], "Unknown Vendor"))
