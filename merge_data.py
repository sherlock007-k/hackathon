import pandas as pd

# Load real dataset (from your network scan processing)
real = pd.read_csv("clean_data.csv")      # your actual collected data

# Load synthetic dataset that we just generated
synthetic = pd.read_csv("synthetic_data.csv")

# Merge both datasets together
merged = pd.concat([real, synthetic], ignore_index=True)

# Shuffle for better training behavior
merged = merged.sample(frac=1).reset_index(drop=True)

# Save final combined dataset
merged.to_csv("training_data.csv", index=False)

print("\n---------------------------")
print(" Real Devices       :", len(real))
print(" Synthetic Devices  :", len(synthetic))
print(" Total Combined     :", len(merged))
print("---------------------------")
print("Saved as training_data.csv successfully! 🎉")
