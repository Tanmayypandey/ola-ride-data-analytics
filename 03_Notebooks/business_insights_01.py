import pandas as pd
import matplotlib.pyplot as plt

file_path = r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\cleaned\ola_feature_engineered.csv"

df = pd.read_csv(
    file_path,
    low_memory=False
)

print("Dataset loaded successfully.")
print("Shape:", df.shape)

total_bookings = len(df)

completed = (
    df["booking_status"] == "Completed"
).sum()

failed_bookings = (
    df["booking_status"] != "Completed"
).sum()

completion_rate = (
    completed / total_bookings
) * 100

failure_rate = (
    failed_bookings / total_bookings
) * 100

print("Total Bookings:", total_bookings)
print("Completed Bookings:", completed)
print("Failed/Unfulfilled Bookings:", failed_bookings)

print("Completion Rate:", round(completion_rate, 2), "%")
print("Failure Rate:", round(failure_rate, 2), "%")
cancellation_analysis = (
    df["booking_status"]
    .value_counts()
    .reindex([
        "Cancelled by Customer",
        "Cancelled by Driver",
        "No Driver Found",
        "Incomplete"
    ])
)

print("\nUnsuccessful Booking Analysis:")
print(cancellation_analysis)

print("\nPercentage:")
print(
    (cancellation_analysis / len(df) * 100)
    .round(2)
)
vehicle_success = (
    df.groupby("vehicle_type")
    .agg(
        total_bookings=("booking_id", "count"),
        completed_rides=("is_completed", "sum")
    )
)

vehicle_success["completion_rate"] = (
    vehicle_success["completed_rides"]
    / vehicle_success["total_bookings"]
    * 100
)

print("\nVehicle Completion Rate:")

print(
    vehicle_success
    .sort_values(
        "completion_rate",
        ascending=False
    )
)
revenue_efficiency = (
    df.groupby("vehicle_type")
    .agg(
        total_revenue=("booking_value", "sum"),
        avg_revenue_per_km=("revenue_per_km", "mean"),
        avg_booking_value=("booking_value", "mean")
    )
)

print("\nRevenue Efficiency by Vehicle:")

print(
    revenue_efficiency
    .sort_values(
        "avg_revenue_per_km",
        ascending=False
    )
)
peak_hours = (
    df["booking_hour"]
    .value_counts()
    .sort_values(ascending=False)
    .head(5)
)

print("\nTop 5 Peak Booking Hours:")

print(peak_hours)
