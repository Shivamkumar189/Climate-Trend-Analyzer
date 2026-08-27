import pandas as pd
import numpy as np

df = pd.read_csv("data/climate_data.csv")

mean = df['temperature'].mean()
std = df['temperature'].std()

df['anomaly'] = abs(df['temperature'] - mean) > 2*std

df.to_csv("outputs/anomaly_output.csv", index=False)

print("✅ Anomaly detection done")