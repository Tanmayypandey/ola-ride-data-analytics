import pandas as pd


# ============================================================
# 1. LOAD CLEANED DATASET
# ============================================================

file_path = r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\cleaned\ola_cleaned.csv"

df = pd.read_csv(file_path, low_memory=False)

print("=" * 60)
print("DATASET VALIDATION REPORT")
print("=" * 60)


# ============================================================
# 2. BASIC DATASET INFORMATION
# ============================================================

print("\n1. DATASET SHAPE")
print("-" * 40)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


print("\n2. COLUMN NAMES")
print("-" * 40)

print(df.columns.tolist())


# ============================================================
# 3. MISSING VALUE ANALYSIS
# ============================================================

print("\n3. MISSING VALUES")
print("-" * 40)

missing_count = df.isnull().sum()

print(missing_count)


print("\n4. MISSING VALUE PERCENTAGE")
print("-" * 40)

missing_percentage = (
    df.isnull()
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(missing_percentage)


# ============================================================
# 4. DUPLICATE ANALYSIS
# ============================================================

print("\n5. DUPLICATE ROWS")
print("-" * 40)

print("Duplicate rows:", df.duplicated().sum())


print("\n6. DUPLICATE BOOKING IDs")
print("-" * 40)

print(
    "Duplicate Booking IDs:",
    df["booking_id"].duplicated().sum()
)


# ============================================================
# 5. INVESTIGATE DUPLICATE BOOKING IDs
# ============================================================

duplicate_bookings = df[
    df["booking_id"].duplicated(keep=False)
].sort_values("booking_id")

print("\n7. DUPLICATE BOOKING RECORDS")
print("-" * 40)

print("Rows containing duplicate Booking IDs:",
      duplicate_bookings.shape[0])


print("\nSample Duplicate Bookings:")
print(
    duplicate_bookings[
        [
            "booking_id",
            "date",
            "time",
            "booking_status",
            "customer_id"
        ]
    ].head(20)
)


print("\nMost Repeated Booking IDs:")
print(
    duplicate_bookings["booking_id"]
    .value_counts()
    .head(20)
)


# ============================================================
# 6. NUMERICAL DATA VALIDATION
# ============================================================

print("\n8. NUMERICAL SUMMARY")
print("-" * 40)

numeric_columns = [
    "booking_value",
    "ride_distance",
    "avg_vtat",
    "avg_ctat",
    "driver_ratings",
    "customer_rating"
]

print(df[numeric_columns].describe())


# ============================================================
# 7. INVALID VALUES
# ============================================================

print("\n9. INVALID DRIVER RATINGS")
print("-" * 40)

invalid_driver_ratings = (
    (df["driver_ratings"] < 1) |
    (df["driver_ratings"] > 5)
).sum()

print(invalid_driver_ratings)


print("\n10. INVALID CUSTOMER RATINGS")
print("-" * 40)

invalid_customer_ratings = (
    (df["customer_rating"] < 1) |
    (df["customer_rating"] > 5)
).sum()

print(invalid_customer_ratings)


print("\n11. NEGATIVE BOOKING VALUES")
print("-" * 40)

print(
    (df["booking_value"] < 0).sum()
)


print("\n12. NEGATIVE RIDE DISTANCES")
print("-" * 40)

print(
    (df["ride_distance"] < 0).sum()
)


# ============================================================
# 8. MISSING BOOKING VALUE BY BOOKING STATUS
# ============================================================

print("\n13. MISSING BOOKING VALUE BY STATUS")
print("-" * 40)

missing_booking_value = (
    df.groupby("booking_status")["booking_value"]
    .apply(lambda x: x.isnull().sum())
)

print(missing_booking_value)


# ============================================================
# 9. MISSING RIDE DISTANCE BY BOOKING STATUS
# ============================================================

print("\n14. MISSING RIDE DISTANCE BY STATUS")
print("-" * 40)

missing_ride_distance = (
    df.groupby("booking_status")["ride_distance"]
    .apply(lambda x: x.isnull().sum())
)

print(missing_ride_distance)


# ============================================================
# 10. CUSTOMER CANCELLATION ANALYSIS
# ============================================================

print("\n15. CUSTOMER CANCELLATION BY STATUS")
print("-" * 40)

customer_cancellation = (
    df.groupby("booking_status")[
        "cancelled_rides_by_customer"
    ].sum()
)

print(customer_cancellation)


# ============================================================
# 11. DRIVER CANCELLATION ANALYSIS
# ============================================================

print("\n16. DRIVER CANCELLATION BY STATUS")
print("-" * 40)

driver_cancellation = (
    df.groupby("booking_status")[
        "cancelled_rides_by_driver"
    ].sum()
)

print(driver_cancellation)


# ============================================================
# 12. CUSTOMER CANCELLATION REASONS
# ============================================================

print("\n17. CUSTOMER CANCELLATION REASONS BY STATUS")
print("-" * 40)

customer_cancel_reasons = (
    df["reason_for_cancelling_by_customer"]
    .notna()
    .groupby(df["booking_status"])
    .sum()
)

print(customer_cancel_reasons)


# ============================================================
# 13. DATE CONVERSION
# ============================================================

print("\n18. DATE CONVERSION")
print("-" * 40)

df["date"] = pd.to_datetime(
    df["date"],
    format="%d-%m-%Y"
)

print("Date conversion completed.")


# ============================================================
# 14. TIME CONVERSION
# ============================================================

print("\n19. TIME CONVERSION")
print("-" * 40)

df["time"] = pd.to_datetime(
    df["time"],
    format="%H:%M:%S"
).dt.time

print("Time conversion completed.")


# ============================================================
# 15. FEATURE ENGINEERING - DATE
# ============================================================

print("\n20. DATE FEATURES")
print("-" * 40)

df["booking_month"] = df["date"].dt.month

df["booking_day"] = df["date"].dt.day

df["booking_day_name"] = df["date"].dt.day_name()

print(
    df[
        [
            "date",
            "booking_month",
            "booking_day",
            "booking_day_name"
        ]
    ].head()
)


# ============================================================
# 16. BOOKING STATUS FLAGS
# ============================================================

print("\n21. BOOKING STATUS FLAGS")
print("-" * 40)

df["is_completed"] = (
    df["booking_status"] == "Completed"
).astype(int)


df["is_cancelled"] = (
    df["booking_status"]
    .str.contains(
        "Cancelled",
        case=False,
        na=False
    )
).astype(int)


df["is_incomplete"] = (
    df["booking_status"] == "Incomplete"
).astype(int)


print(
    df[
        [
            "booking_status",
            "is_completed",
            "is_cancelled",
            "is_incomplete"
        ]
    ].head(20)
)


# ============================================================
# 17. FINAL DATASET CHECK
# ============================================================

print("\n22. FINAL DATASET SHAPE")
print("-" * 40)

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


print("\n23. FINAL COLUMNS")
print("-" * 40)

print(df.columns.tolist())


# ============================================================
# 18. SAVE VALIDATED DATASET
# ============================================================

output_path = (
    r"C:\Users\hp\Desktop\ola_ride_dataAnalysis"
    r"\data\raw\cleaned\ola_validated.csv"
)

df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 60)
print("VALIDATION COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nValidated dataset saved at:")
print(output_path)