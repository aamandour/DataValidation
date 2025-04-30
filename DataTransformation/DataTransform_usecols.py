import pandas as pd

# Read the CSV but only load needed columns
df = pd.read_csv('bc_trip259172515_230215.csv', usecols=[
    'EVENT_NO_TRIP', 'OPD_DATE', 'VEHICLE_ID', 'METERS', 'ACT_TIME', 'GPS_LONGITUDE', 'GPS_LATITUDE'
])

# Show the DataFrame info
print(df.info())

# Print the list of columns
print(df.columns)

# Print the number of breadcrumb records
print(f"Total number of breadcrumb records: {len(df)}")
