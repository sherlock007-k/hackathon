import pandas as pd
import numpy as np

LOG_FILE = "honeypot_logs.csv"

def detect_anomalies():
    try:
        df = pd.read_csv(LOG_FILE)
    except:
        print("⚠ No honeypot logs found yet.")
        return

    # Count requests per IP
    freq = df['ip'].value_counts()
    mean = freq.mean()
    std = freq.std()

    anomaly_report = []

    for ip, count in freq.items():
        # Z-Score = how far this IP deviates from normal
        if std == 0:
            z = 0
        else:
            z = (count - mean) / std  

        status = "Normal"
        if z > 1.5: status = "Suspicious"
        if z > 2.5: status = "Critical Threat"

        anomaly_report.append([ip, count, round(z,2), status])

    result_df = pd.DataFrame(anomaly_report, columns=["IP", "Hits", "Z-Score", "Threat Level"])
    result_df.to_csv("anomaly_report.csv", index=False)

    print("\n📊 Anomaly Detection Completed")
    print(result_df)
    print("\nSaved as anomaly_report.csv")

if __name__ == "__main__":
    detect_anomalies()
