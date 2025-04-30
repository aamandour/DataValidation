import pandas as pd

# Step 1: Load the dataset with selected columns
df = pd.read_csv('bc_trip259172515_230215.csv', usecols=['EVENT_NO_TRIP', 'OPD_DATE', 'VEHICLE_ID', 'METERS', 'ACT_TIME', 'GPS_LONGITUDE', 'GPS_LATITUDE'])

# Step 2: Correctly parse OPD_DATE
df['OPD_DATE'] = pd.to_datetime(df['OPD_DATE'], format='%d%b%Y:%H:%M:%S')

# Step 3 (A): Apply .apply() to create TIMESTAMP using Timestamp + Timedelta
def create_timestamp(row):
    base = pd.Timestamp(row['OPD_DATE'])                     # i. create datetime
    offset = pd.Timedelta(seconds=row['ACT_TIME'])           # ii. create timedelta
    return base + offset                                      # iii. combine

df['TIMESTAMP'] = df.apply(create_timestamp, axis=1)

# Step 4 (B): Drop OPD_DATE and ACT_TIME
df = df.drop(columns=['OPD_DATE', 'ACT_TIME'])

# Step 5 (C): Show final result
print(df.head())         # show the first few rows with final columns
print(df.info())         # confirm structure: 6 columns
