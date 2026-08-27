import pandas as pd
import numpy as np

# Create date range
dates = pd.date_range(start="2015-01-01", end="2022-12-31")

# Generate seasonal temperature
temperature = 25 + 10*np.sin(2*np.pi*dates.dayofyear/365) + np.random.normal(0,2,len(dates))

# Generate rainfall
rainfall = np.random.gamma(2,2,len(dates))

# Generate humidity
humidity = np.random.uniform(40,90,len(dates))

df = pd.DataFrame({
    "date": dates,
    "temperature": temperature,
    "rainfall": rainfall,
    "humidity": humidity
})

# Save file
df.to_csv("data/climate_data.csv", index=False)

print("✅ Dataset created successfully!")