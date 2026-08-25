import pandas as pd

file_path = r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\cleaned\ola_validated.csv"

df = pd.read_csv(file_path, low_memory=False)

print("Dataset loaded successfully.")
print("Shape:", df.shape)
df["date"] = pd.to_datetime(
    df["date"],
    format="%Y-%m-%d"
)

df["time"] = pd.to_datetime(
    df["time"],
    format="%H:%M:%S"
).dt.time
# 1. Booking Hour
df["booking_hour"] = pd.to_datetime(
    df["time"].astype(str)
).dt.hour


# 2. Time of Day
df["time_of_day"] = pd.cut(
    df["booking_hour"],
    bins=[-1, 6, 12, 17, 21, 24],
    labels=[
        "Night",
        "Morning",
        "Afternoon",
        "Evening",
        "Late Night"
    ]
)


# 3. Cancellation Type
df["cancellation_type"] = "Not Cancelled"

df.loc[
    df["booking_status"] == "Cancelled by Customer",
    "cancellation_type"
] = "Customer"

df.loc[
    df["booking_status"] == "Cancelled by Driver",
    "cancellation_type"
] = "Driver"

df.loc[
    df["booking_status"] == "No Driver Found",
    "cancellation_type"
] = "No Driver Found"


# 4. Revenue per KM
df["revenue_per_km"] = (
    df["booking_value"] / df["ride_distance"]
)


# 5. Weekend Flag
df["is_weekend"] = (
    df["date"].dt.dayofweek >= 5
).astype(int)


# Check the new features
print(
    df[
        [
            "booking_hour",
            "time_of_day",
            "cancellation_type",
            "revenue_per_km",
            "is_weekend"
        ]
    ].head(20)
)
output_path = r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\cleaned\ola_feature_engineered.csv"

df.to_csv(
    output_path,
    index=False
)

print("\nFeature-engineered dataset saved successfully.")
print(output_path)
print("Final Shape:", df.shape)