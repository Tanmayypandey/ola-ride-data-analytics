import pandas as pd


# ============================================================
# 1. FILE PATHS
# ============================================================

input_path = (
    r"C:\Users\hp\Desktop\ola_ride_dataAnalysis"
    r"\data\raw\cleaned\ola_cleaned.csv"
)

output_path = (
    r"C:\Users\hp\Desktop\ola_ride_dataAnalysis"
    r"\data\raw\cleaned\ola_validated.csv"
)


# ============================================================
# 2. LOAD CLEANED DATASET
# ============================================================

df = pd.read_csv(
    input_path,
    low_memory=False
)

print("=" * 70)
print("OLA DATASET VALIDATION REPORT")
print("=" * 70)

print("\nDataset loaded successfully.")


# ============================================================
# 3. BASIC DATASET INFORMATION
# ============================================================

print("\n1. DATASET SHAPE")
print("-" * 50)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n2. COLUMN NAMES")
print("-" * 50)

for number, column in enumerate(df.columns, start=1):
    print(f"{number}. {column}")


# ============================================================
# 4. REQUIRED COLUMN VALIDATION
# ============================================================

required_columns = [
    "date",
    "time",
    "booking_id",
    "booking_status",
    "customer_id",
    "vehicle_type",
    "pickup_location",
    "drop_location",
    "avg_vtat",
    "avg_ctat",
    "cancelled_rides_by_customer",
    "reason_for_cancelling_by_customer",
    "cancelled_rides_by_driver",
    "driver_cancellation_reason",
    "incomplete_rides",
    "incomplete_rides_reason",
    "booking_value",
    "ride_distance",
    "driver_ratings",
    "customer_rating",
    "payment_method"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

print("\n3. REQUIRED COLUMN VALIDATION")
print("-" * 50)

if missing_columns:
    print("Missing required columns:")
    print(missing_columns)

    raise ValueError(
        "Dataset validation stopped because required columns are missing."
    )

print("All required columns are available.")


# ============================================================
# 5. MISSING VALUE ANALYSIS
# ============================================================

print("\n4. MISSING VALUE COUNT")
print("-" * 50)

missing_count = (
    df.isnull()
    .sum()
    .sort_values(ascending=False)
)

print(missing_count)

print("\n5. MISSING VALUE PERCENTAGE")
print("-" * 50)

missing_percentage = (
    df.isnull()
    .mean()
    .mul(100)
    .round(2)
    .sort_values(ascending=False)
)

print(missing_percentage)


# ============================================================
# 6. EXACT DUPLICATE ROW ANALYSIS
# ============================================================

duplicate_rows = df.duplicated().sum()

print("\n6. EXACT DUPLICATE ROWS")
print("-" * 50)
print("Exact duplicate rows:", duplicate_rows)


# ============================================================
# 7. DUPLICATE BOOKING ID ANALYSIS
# ============================================================

duplicate_booking_count = (
    df["booking_id"]
    .duplicated()
    .sum()
)

duplicate_booking_records = (
    df[
        df["booking_id"].duplicated(keep=False)
    ]
    .sort_values("booking_id")
)

repeated_booking_ids = (
    duplicate_booking_records["booking_id"]
    .nunique()
)

print("\n7. BOOKING ID UNIQUENESS CHECK")
print("-" * 50)

print("Total records:", len(df))
print(
    "Unique original Booking IDs:",
    df["booking_id"].nunique()
)
print(
    "Additional repeated Booking ID occurrences:",
    duplicate_booking_count
)
print(
    "Number of Booking IDs appearing more than once:",
    repeated_booking_ids
)
print(
    "Rows containing repeated Booking IDs:",
    len(duplicate_booking_records)
)

if len(duplicate_booking_records) > 0:
    print("\nSample records containing repeated Booking IDs:")

    duplicate_display_columns = [
        "booking_id",
        "date",
        "time",
        "booking_status",
        "customer_id",
        "vehicle_type"
    ]

    print(
        duplicate_booking_records[
            duplicate_display_columns
        ].head(20)
    )

    print("\nMost frequently repeated Booking IDs:")

    print(
        duplicate_booking_records["booking_id"]
        .value_counts()
        .head(20)
    )


# ============================================================
# 8. CREATE UNIQUE ANALYTICAL RECORD ID
# ============================================================

# The original booking_id is retained because repeated IDs
# represent different records rather than exact duplicate rows.

if "booking_record_id" in df.columns:
    df = df.drop(
        columns=["booking_record_id"]
    )

df.insert(
    0,
    "booking_record_id",
    [
        f"BR{i:06d}"
        for i in range(1, len(df) + 1)
    ]
)

print("\n8. UNIQUE ANALYTICAL RECORD ID")
print("-" * 50)

print(
    "Unique Booking Record IDs:",
    df["booking_record_id"].nunique()
)

print(
    "Duplicate Booking Record IDs:",
    df["booking_record_id"].duplicated().sum()
)


# ============================================================
# 9. NUMERICAL DATA VALIDATION
# ============================================================

numeric_columns = [
    "booking_value",
    "ride_distance",
    "avg_vtat",
    "avg_ctat",
    "driver_ratings",
    "customer_rating"
]

print("\n9. NUMERICAL SUMMARY")
print("-" * 50)

print(
    df[numeric_columns]
    .describe()
    .round(2)
)


# ============================================================
# 10. INVALID VALUE CHECKS
# ============================================================

invalid_driver_ratings = (
    (
        (df["driver_ratings"] < 1)
        | (df["driver_ratings"] > 5)
    )
    & df["driver_ratings"].notna()
).sum()

invalid_customer_ratings = (
    (
        (df["customer_rating"] < 1)
        | (df["customer_rating"] > 5)
    )
    & df["customer_rating"].notna()
).sum()

negative_booking_values = (
    df["booking_value"] < 0
).sum()

negative_ride_distances = (
    df["ride_distance"] < 0
).sum()

negative_vtat = (
    df["avg_vtat"] < 0
).sum()

negative_ctat = (
    df["avg_ctat"] < 0
).sum()

print("\n10. INVALID VALUE CHECKS")
print("-" * 50)

print(
    "Invalid driver ratings:",
    invalid_driver_ratings
)

print(
    "Invalid customer ratings:",
    invalid_customer_ratings
)

print(
    "Negative booking values:",
    negative_booking_values
)

print(
    "Negative ride distances:",
    negative_ride_distances
)

print(
    "Negative average VTAT values:",
    negative_vtat
)

print(
    "Negative average CTAT values:",
    negative_ctat
)


# ============================================================
# 11. BOOKING STATUS VALIDATION
# ============================================================

expected_booking_statuses = [
    "Completed",
    "Cancelled by Driver",
    "Cancelled by Customer",
    "No Driver Found",
    "Incomplete"
]

invalid_booking_statuses = (
    df.loc[
        ~df["booking_status"].isin(
            expected_booking_statuses
        ),
        "booking_status"
    ]
    .dropna()
    .unique()
)

print("\n11. BOOKING STATUS VALIDATION")
print("-" * 50)

print("\nBooking status distribution:")
print(
    df["booking_status"]
    .value_counts(dropna=False)
)

if len(invalid_booking_statuses) == 0:
    print("\nNo invalid booking status found.")
else:
    print("\nInvalid booking statuses:")
    print(invalid_booking_statuses)


# ============================================================
# 12. MISSING VALUES BY BOOKING STATUS
# ============================================================

print("\n12. MISSING BOOKING VALUE BY STATUS")
print("-" * 50)

missing_booking_value = (
    df.groupby("booking_status")[
        "booking_value"
    ]
    .apply(lambda column: column.isnull().sum())
)

print(missing_booking_value)

print("\n13. MISSING RIDE DISTANCE BY STATUS")
print("-" * 50)

missing_ride_distance = (
    df.groupby("booking_status")[
        "ride_distance"
    ]
    .apply(lambda column: column.isnull().sum())
)

print(missing_ride_distance)

print("\n14. MISSING PAYMENT METHOD BY STATUS")
print("-" * 50)

missing_payment_method = (
    df.groupby("booking_status")[
        "payment_method"
    ]
    .apply(lambda column: column.isnull().sum())
)

print(missing_payment_method)


# ============================================================
# 13. CANCELLATION VALIDATION
# ============================================================

print("\n15. CUSTOMER CANCELLATION BY STATUS")
print("-" * 50)

customer_cancellation = (
    df.groupby("booking_status")[
        "cancelled_rides_by_customer"
    ]
    .sum()
)

print(customer_cancellation)

print("\n16. DRIVER CANCELLATION BY STATUS")
print("-" * 50)

driver_cancellation = (
    df.groupby("booking_status")[
        "cancelled_rides_by_driver"
    ]
    .sum()
)

print(driver_cancellation)

print("\n17. CUSTOMER CANCELLATION REASONS BY STATUS")
print("-" * 50)

customer_cancel_reasons = (
    df[
        "reason_for_cancelling_by_customer"
    ]
    .notna()
    .groupby(df["booking_status"])
    .sum()
)

print(customer_cancel_reasons)

print("\n18. DRIVER CANCELLATION REASONS BY STATUS")
print("-" * 50)

driver_cancel_reasons = (
    df["driver_cancellation_reason"]
    .notna()
    .groupby(df["booking_status"])
    .sum()
)

print(driver_cancel_reasons)


# ============================================================
# 14. DATE CONVERSION AND VALIDATION
# ============================================================

print("\n19. DATE CONVERSION")
print("-" * 50)

df["date"] = pd.to_datetime(
    df["date"],
    dayfirst=True,
    errors="coerce"
)

invalid_dates = df["date"].isna().sum()

print(
    "Invalid dates after conversion:",
    invalid_dates
)

if df["date"].notna().any():
    print(
        "Minimum date:",
        df["date"].min().date()
    )

    print(
        "Maximum date:",
        df["date"].max().date()
    )


# ============================================================
# 15. TIME CONVERSION AND VALIDATION
# ============================================================

print("\n20. TIME CONVERSION")
print("-" * 50)

converted_time = pd.to_datetime(
    df["time"].astype(str),
    format="%H:%M:%S",
    errors="coerce"
)

invalid_times = converted_time.isna().sum()

df["time"] = converted_time.dt.strftime(
    "%H:%M:%S"
)

print(
    "Invalid times after conversion:",
    invalid_times
)


# ============================================================
# 16. DATE FEATURES
# ============================================================

print("\n21. DATE FEATURES")
print("-" * 50)

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
# 17. BOOKING STATUS FLAGS
# ============================================================

df["is_completed"] = (
    df["booking_status"]
    .eq("Completed")
    .astype(int)
)

df["is_cancelled"] = (
    df["booking_status"]
    .str.contains(
        "Cancelled",
        case=False,
        na=False
    )
    .astype(int)
)

df["is_incomplete"] = (
    df["booking_status"]
    .eq("Incomplete")
    .astype(int)
)

print("\n22. BOOKING STATUS FLAGS")
print("-" * 50)

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
# 18. FINAL VALIDATION SUMMARY
# ============================================================

print("\n23. FINAL VALIDATION SUMMARY")
print("-" * 50)

print("Final rows:", df.shape[0])
print("Final columns:", df.shape[1])
print("Exact duplicate rows:", df.duplicated().sum())

print(
    "Duplicate Booking Record IDs:",
    df["booking_record_id"]
    .duplicated()
    .sum()
)

print(
    "Missing Booking Record IDs:",
    df["booking_record_id"]
    .isna()
    .sum()
)


# ============================================================
# 19. SAVE VALIDATED DATASET
# ============================================================

df.to_csv(
    output_path,
    index=False
)

print("\n" + "=" * 70)
print("VALIDATION COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nValidated dataset saved at:")
print(output_path)