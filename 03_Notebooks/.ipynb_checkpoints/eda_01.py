import pandas as pd


# ============================================================
# 1. LOAD FEATURE-ENGINEERED DATASET
# ============================================================

file_path = r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\cleaned\ola_feature_engineered.csv"

df = pd.read_csv(
    file_path,
    low_memory=False
)

print("Dataset loaded successfully.")
print("Shape:", df.shape)


# ============================================================
# 2. BOOKING STATUS ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("BOOKING STATUS ANALYSIS")
print("=" * 60)

print("\nBooking Status Distribution:")

print(
    df["booking_status"].value_counts()
)


print("\nBooking Status Percentage:")

print(
    df["booking_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# ============================================================
# 3. REVENUE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("REVENUE ANALYSIS")
print("=" * 60)

print("\nTotal Revenue:")

print(
    df["booking_value"].sum()
)


print("\nAverage Booking Value:")

print(
    df["booking_value"].mean()
)


print("\nMedian Booking Value:")

print(
    df["booking_value"].median()
)


print("\nRevenue by Vehicle Type:")

print(
    df.groupby("vehicle_type")["booking_value"]
    .sum()
    .sort_values(ascending=False)
)


# ============================================================
# 4. VEHICLE PERFORMANCE ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("VEHICLE PERFORMANCE ANALYSIS")
print("=" * 60)

vehicle_analysis = (
    df.groupby("vehicle_type")
    .agg(
        total_bookings=("booking_id", "count"),

        completed_rides=("is_completed", "sum"),

        cancelled_rides=("is_cancelled", "sum"),

        avg_booking_value=("booking_value", "mean"),

        avg_distance=("ride_distance", "mean"),

        avg_driver_rating=("driver_ratings", "mean"),

        avg_customer_rating=("customer_rating", "mean")
    )
)

print(
    vehicle_analysis.sort_values(
        "total_bookings",
        ascending=False
    )
)


# ============================================================
# 5. TIME ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("TIME ANALYSIS")
print("=" * 60)

print("\nBookings by Time of Day:")

print(
    df["time_of_day"]
    .value_counts()
)


print("\nBookings by Hour:")

print(
    df["booking_hour"]
    .value_counts()
    .sort_index()
)


print("\nBookings by Day:")

print(
    df["booking_day_name"]
    .value_counts()
)


# ============================================================
# 6. LOCATION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("LOCATION ANALYSIS")
print("=" * 60)

print("\nTop 10 Pickup Locations:")

print(
    df["pickup_location"]
    .value_counts()
    .head(10)
)


print("\nTop 10 Drop Locations:")

print(
    df["drop_location"]
    .value_counts()
    .head(10)
)


# ============================================================
# 7. TOP ROUTES
# ============================================================

print("\nTop 10 Routes:")

top_routes = (
    df.groupby(
        [
            "pickup_location",
            "drop_location"
        ]
    )
    .size()
    .sort_values(ascending=False)
    .head(10)
)

print(top_routes)


# ============================================================
# 8. FINAL CHECK
# ============================================================

print("\n" + "=" * 60)
print("EDA BASIC ANALYSIS COMPLETED")
print("=" * 60)