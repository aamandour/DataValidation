import pandas as pd

# Load cleaned file from previous step
df = pd.read_csv('bc_trip259172515_230215.csv', usecols=[
    'EVENT_NO_TRIP', 'OPD_DATE', 'VEHICLE_ID', 'METERS',
    'ACT_TIME', 'GPS_LONGITUDE', 'GPS_LATITUDE'
])

# Decode OPD_DATE + ACT_TIME into TIMESTAMP
df['OPD_DATE'] = pd.to_datetime(df['OPD_DATE'], format='%d%b%Y:%H:%M:%S')

def create_timestamp(row):
    return pd.Timestamp(row['OPD_DATE']) + pd.Timedelta(seconds=row['ACT_TIME'])

df['TIMESTAMP'] = df.apply(create_timestamp, axis=1)

# Drop OPD_DATE and ACT_TIME
df = df.drop(columns=['OPD_DATE', 'ACT_TIME'])

# Step 1: Calculate differences (distance and time deltas)
df['dMETERS'] = df['METERS'].diff()
df['dTIME'] = df['TIMESTAMP'].diff().dt.total_seconds()

# Step 2: Calculate SPEED (meters per second)
# If dTIME is 0 or NaN, treat SPEED as 0.0
df['SPEED'] = df.apply(
    lambda row: row['dMETERS'] / row['dTIME'] if pd.notnull(row['dTIME']) and row['dTIME'] > 0 else 0.0,
    axis=1
)

# Step 3: Drop intermediate columns
df = df.drop(columns=['dMETERS', 'dTIME'])

# Step 4: Show sample and structure
print(df[['METERS', 'TIMESTAMP', 'SPEED']].head())
print(df.info())

# Step 5: Summary speed stats (include SPEED=0.0 rows)
print("\n--- Speed Statistics ---")
print(f"Minimum speed: {df['SPEED'].min():.2f} m/s")
print(f"Maximum speed: {df['SPEED'].max():.2f} m/s")
print(f"Average speed: {df['SPEED'].mean():.2f} m/s")

