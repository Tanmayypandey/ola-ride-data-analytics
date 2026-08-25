import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD FEATURE-ENGINEERED DATA
# ============================================================

file_path = r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\cleaned\ola_feature_engineered.csv"

df = pd.read_csv(
    file_path,
    low_memory=False
)

print("Dataset loaded successfully.")
print("Shape:", df.shape)


# ============================================================
# CREATE VISUALIZATION FOLDER
# ============================================================

output_folder = r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\visualizations"

import os

os.makedirs(output_folder, exist_ok=True)


# ============================================================
# 2. BOOKING STATUS VISUALIZATION
# ============================================================

booking_status = (
    df["booking_status"]
    .value_counts()
)

plt.figure(figsize=(10, 6))

plt.bar(
    booking_status.index,
    booking_status.values
)

plt.title("Ola Booking Status Distribution")
plt.xlabel("Booking Status")
plt.ylabel("Number of Bookings")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "01_booking_status_distribution.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 3. REVENUE BY VEHICLE TYPE
# ============================================================

revenue_vehicle = (
    df.groupby("vehicle_type")["booking_value"]
    .sum()
    .sort_values(ascending=True)
)

plt.figure(figsize=(10, 6))

plt.barh(
    revenue_vehicle.index,
    revenue_vehicle.values
)

plt.title("Revenue by Vehicle Type")
plt.xlabel("Total Revenue")
plt.ylabel("Vehicle Type")

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "02_revenue_by_vehicle_type.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 4. HOURLY BOOKING DEMAND
# ============================================================

hourly_bookings = (
    df["booking_hour"]
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(12, 6))

plt.plot(
    hourly_bookings.index,
    hourly_bookings.values,
    marker="o"
)

plt.title("Ola Booking Demand by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Bookings")

plt.xticks(range(24))

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "03_hourly_booking_demand.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 5. BOOKING DEMAND BY DAY
# ============================================================

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

daily_bookings = (
    df["booking_day_name"]
    .value_counts()
    .reindex(day_order)
)

plt.figure(figsize=(10, 6))

plt.bar(
    daily_bookings.index,
    daily_bookings.values
)

plt.title("Ola Booking Demand by Day")
plt.xlabel("Day of Week")
plt.ylabel("Number of Bookings")

plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "04_booking_demand_by_day.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 6. CANCELLATION ANALYSIS
# ============================================================

cancellation_data = {
    "Customer Cancellation":
        (
            df["booking_status"] ==
            "Cancelled by Customer"
        ).sum(),

    "Driver Cancellation":
        (
            df["booking_status"] ==
            "Cancelled by Driver"
        ).sum(),

    "No Driver Found":
        (
            df["booking_status"] ==
            "No Driver Found"
        ).sum()
}

cancellation_series = pd.Series(
    cancellation_data
)

plt.figure(figsize=(10, 6))

plt.bar(
    cancellation_series.index,
    cancellation_series.values
)

plt.title("Ola Booking Failure / Cancellation Analysis")
plt.xlabel("Cancellation Type")
plt.ylabel("Number of Bookings")

plt.xticks(rotation=15)

plt.tight_layout()

plt.savefig(
    os.path.join(
        output_folder,
        "05_cancellation_analysis.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("ALL 5 VISUALIZATIONS CREATED SUCCESSFULLY")
print("=" * 60)

print("\nSaved inside:")
print(output_folder)