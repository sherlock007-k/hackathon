import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("clean_data.csv")

# If dataset small → add dummy sample data for better visualization
dummy = pd.DataFrame([
    ["192.168.1.50","Unknown Vendor",5,"[23,80,8080]",75,"High","High Risk"],
    ["192.168.1.21","ESP Device",3,"[80]",40,"Moderate","Medium Risk"],
    ["192.168.1.78","D-Link",1,"[443]",10,"Secure","Low Risk"],
    ["192.168.1.90","Mi Home",4,"[80,8080]",55,"Medium","Medium Risk"]
], columns=df.columns)

df = pd.concat([df, dummy], ignore_index=True)

print("Dataset Loaded. Total entries:", len(df))

# --------------------------------------
# PLOT 1 : Risk Label Distribution
# --------------------------------------
plt.figure(figsize=(6,4))
sns.countplot(data=df, x="risk_label", palette="viridis")
plt.title("Device Risk Distribution")
plt.xlabel("Risk")
plt.ylabel("Number of Devices")
plt.tight_layout()
plt.show()

# --------------------------------------
# PLOT 2 : Vendor Distribution
# --------------------------------------
plt.figure(figsize=(7,4))
top_vendors = df['vendor'].value_counts().head(10)
top_vendors.plot(kind='bar')
plt.title("Top Vendors in Network")
plt.xlabel("Vendor")
plt.ylabel("Device Count")
plt.tight_layout()
plt.show()

# --------------------------------------
# PLOT 3 : Risk Score Histogram
# --------------------------------------
plt.figure(figsize=(6,4))
sns.histplot(df['risk_score'], bins=10, kde=True)
plt.title("Risk Score Spread")
plt.xlabel("Risk Score")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# --------------------------------------
# PLOT 4 : Ports Count vs Risk
# --------------------------------------
plt.figure(figsize=(6,4))
sns.scatterplot(data=df, x="ports_count", y="risk_score", hue="risk_label")
plt.title("Ports vs Risk Score Relation")
plt.tight_layout()
plt.show()
