import pandas as pd

def preprocess():
    df = pd.read_csv("iot_dataset.csv")

    # Create ML friendly label from risk_score
    df['risk_label'] = df['risk_score'].apply(
        lambda x: "High" if x>=70 else "Medium" if x>=30 else "Low"
    )

    df.to_csv("clean_data.csv", index=False)
    print("✔ clean_data.csv generated successfully!")

if __name__ == "__main__":
    preprocess()
