import pandas as pd


# ============================================================
# 1. FILE PATH
# ============================================================

file_path = (
    r"C:\Users\hp\Desktop\ola_ride_dataAnalysis"
    r"\data\raw\cleaned\ola_feature_engineered.csv"
)


# ============================================================
# 2. LOAD FEATURE-ENGINEERED DATASET
# ============================================================

df = pd.read_csv(
    file_path,
    low_memory=False
)

print("=" * 70)
print("OLA RIDE BUSINESS INSIGHTS REPORT")
print("=" * 70)

print("\nDataset loaded successfully.")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# 3. REQUIRED COLUMN VALIDATION
# ============================================================

required_columns = [
    "booking_id",
    "booking_status",
    "vehicle_type",
    "booking_value",
    "ride_distance",
    "booking_hour",
    "revenue_per_km",
    "pickup_location",
    "drop_location",
    "payment_method",
    "customer_rating",
    "driver_ratings",
    "is_completed"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    print("\nMissing required columns:")
    print(missing_columns)

    raise ValueError(
        "Business insight generation stopped because columns are missing."
    )

print("\nAll required analytical columns are available.")


# ============================================================
# 4. ENSURE UNIQUE ANALYTICAL RECORD ID EXISTS
# ============================================================

if "booking_record_id" not in df.columns:
    df.insert(
        0,
        "booking_record_id",
        [
            f"BR{i:06d}"
            for i in range(1, len(df) + 1)
        ]
    )

print(
    "Unique analytical records:",
    df["booking_record_id"].nunique()
)


# ============================================================
# 5. OVERALL BOOKING KPIs
# ============================================================

total_bookings = len(df)

completed_bookings = (
    df["booking_status"]
    .eq("Completed")
    .sum()
)

unfulfilled_bookings = (
    df["booking_status"]
    .ne("Completed")
    .sum()
)

completion_rate = (
    completed_bookings
    / total_bookings
    * 100
)

unfulfilled_rate = (
    unfulfilled_bookings
    / total_bookings
    * 100
)

print("\n1. OVERALL BOOKING KPIs")
print("-" * 50)

print(
    "Total Booking Records:",
    f"{total_bookings:,}"
)

print(
    "Completed Rides:",
    f"{completed_bookings:,}"
)

print(
    "Unfulfilled or Incomplete Bookings:",
    f"{unfulfilled_bookings:,}"
)

print(
    "Completion Rate:",
    f"{completion_rate:.2f}%"
)

print(
    "Unfulfilled Rate:",
    f"{unfulfilled_rate:.2f}%"
)


# ============================================================
# 6. BOOKING STATUS DISTRIBUTION
# ============================================================

booking_status_order = [
    "Completed",
    "Cancelled by Driver",
    "Cancelled by Customer",
    "No Driver Found",
    "Incomplete"
]

booking_status_count = (
    df["booking_status"]
    .value_counts()
    .reindex(
        booking_status_order,
        fill_value=0
    )
)

booking_status_percentage = (
    booking_status_count
    .div(total_bookings)
    .mul(100)
    .round(2)
)

booking_status_summary = pd.DataFrame({
    "booking_count": booking_status_count,
    "percentage": booking_status_percentage
})

print("\n2. BOOKING STATUS DISTRIBUTION")
print("-" * 50)
print(booking_status_summary)


# ============================================================
# 7. CANCELLATION AND FAILURE KPIs
# ============================================================

driver_cancellations = booking_status_count[
    "Cancelled by Driver"
]

customer_cancellations = booking_status_count[
    "Cancelled by Customer"
]

no_driver_found = booking_status_count[
    "No Driver Found"
]

incomplete_rides = booking_status_count[
    "Incomplete"
]

driver_cancellation_rate = (
    driver_cancellations
    / total_bookings
    * 100
)

customer_cancellation_rate = (
    customer_cancellations
    / total_bookings
    * 100
)

no_driver_found_rate = (
    no_driver_found
    / total_bookings
    * 100
)

incomplete_ride_rate = (
    incomplete_rides
    / total_bookings
    * 100
)

print("\n3. CANCELLATION AND FAILURE KPIs")
print("-" * 50)

print(
    "Driver Cancellations:",
    f"{driver_cancellations:,}",
    f"({driver_cancellation_rate:.2f}%)"
)

print(
    "Customer Cancellations:",
    f"{customer_cancellations:,}",
    f"({customer_cancellation_rate:.2f}%)"
)

print(
    "No Driver Found:",
    f"{no_driver_found:,}",
    f"({no_driver_found_rate:.2f}%)"
)

print(
    "Incomplete Rides:",
    f"{incomplete_rides:,}",
    f"({incomplete_ride_rate:.2f}%)"
)


# ============================================================
# 8. REVENUE KPIs
# ============================================================

gross_booking_value = (
    df["booking_value"]
    .sum()
)

completed_rides_df = (
    df[
        df["booking_status"]
        .eq("Completed")
    ]
    .copy()
)

realized_revenue = (
    completed_rides_df[
        "booking_value"
    ]
    .sum()
)

average_gross_booking_value = (
    df["booking_value"]
    .mean()
)

average_completed_booking_value = (
    completed_rides_df[
        "booking_value"
    ]
    .mean()
)

median_completed_booking_value = (
    completed_rides_df[
        "booking_value"
    ]
    .median()
)

incomplete_ride_value = (
    df.loc[
        df["booking_status"].eq("Incomplete"),
        "booking_value"
    ]
    .sum()
)

print("\n4. REVENUE KPIs")
print("-" * 50)

print(
    "Gross Booking Value:",
    f"₹{gross_booking_value:,.2f}"
)

print(
    "Realized Revenue from Completed Rides:",
    f"₹{realized_revenue:,.2f}"
)

print(
    "Value Associated with Incomplete Rides:",
    f"₹{incomplete_ride_value:,.2f}"
)

print(
    "Average Gross Booking Value:",
    f"₹{average_gross_booking_value:,.2f}"
)

print(
    "Average Completed Booking Value:",
    f"₹{average_completed_booking_value:,.2f}"
)

print(
    "Median Completed Booking Value:",
    f"₹{median_completed_booking_value:,.2f}"
)


# ============================================================
# 9. VEHICLE COMPLETION PERFORMANCE
# ============================================================

vehicle_success = (
    df.groupby("vehicle_type")
    .agg(
        total_booking_records=(
            "booking_record_id",
            "count"
        ),
        completed_rides=(
            "is_completed",
            "sum"
        )
    )
)

vehicle_success["completion_rate"] = (
    vehicle_success["completed_rides"]
    / vehicle_success["total_booking_records"]
    * 100
)

vehicle_success = (
    vehicle_success
    .sort_values(
        "completion_rate",
        ascending=False
    )
)

print("\n5. VEHICLE COMPLETION PERFORMANCE")
print("-" * 50)

print(
    vehicle_success.round(2)
)


# ============================================================
# 10. GROSS VALUE BY VEHICLE TYPE
# ============================================================

gross_value_by_vehicle = (
    df.groupby("vehicle_type")
    .agg(
        total_booking_records=(
            "booking_record_id",
            "count"
        ),
        gross_booking_value=(
            "booking_value",
            "sum"
        ),
        average_booking_value=(
            "booking_value",
            "mean"
        ),
        average_revenue_per_km=(
            "revenue_per_km",
            "mean"
        )
    )
    .sort_values(
        "gross_booking_value",
        ascending=False
    )
)

print("\n6. GROSS BOOKING VALUE BY VEHICLE")
print("-" * 50)

print(
    gross_value_by_vehicle.round(2)
)


# ============================================================
# 11. REALIZED REVENUE BY VEHICLE TYPE
# ============================================================

completed_vehicle_revenue = (
    completed_rides_df
    .groupby("vehicle_type")
    .agg(
        completed_rides=(
            "booking_record_id",
            "count"
        ),
        realized_revenue=(
            "booking_value",
            "sum"
        ),
        average_booking_value=(
            "booking_value",
            "mean"
        ),
        average_revenue_per_km=(
            "revenue_per_km",
            "mean"
        )
    )
    .sort_values(
        "realized_revenue",
        ascending=False
    )
)

print("\n7. REALIZED REVENUE BY VEHICLE")
print("-" * 50)

print(
    completed_vehicle_revenue.round(2)
)


# ============================================================
# 12. PEAK BOOKING HOURS
# ============================================================

peak_hours = (
    df["booking_hour"]
    .value_counts()
    .sort_values(ascending=False)
    .head(5)
)

print("\n8. TOP FIVE PEAK BOOKING HOURS")
print("-" * 50)

print(peak_hours)

highest_peak_hour = peak_hours.index[0]
highest_peak_bookings = peak_hours.iloc[0]

print(
    "\nHighest peak hour:",
    f"{highest_peak_hour}:00"
)

print(
    "Bookings during the highest peak hour:",
    f"{highest_peak_bookings:,}"
)


# ============================================================
# 13. TIME-OF-DAY ANALYSIS
# ============================================================

if "time_of_day" in df.columns:
    time_of_day_analysis = (
        df.groupby("time_of_day")
        .agg(
            total_bookings=(
                "booking_record_id",
                "count"
            ),
            completed_rides=(
                "is_completed",
                "sum"
            ),
            gross_booking_value=(
                "booking_value",
                "sum"
            )
        )
    )

    time_of_day_analysis[
        "completion_rate"
    ] = (
        time_of_day_analysis[
            "completed_rides"
        ]
        / time_of_day_analysis[
            "total_bookings"
        ]
        * 100
    )

    time_of_day_analysis = (
        time_of_day_analysis
        .sort_values(
            "total_bookings",
            ascending=False
        )
    )

    print("\n9. TIME-OF-DAY PERFORMANCE")
    print("-" * 50)

    print(
        time_of_day_analysis.round(2)
    )


# ============================================================
# 14. TOP PICKUP LOCATIONS
# ============================================================

top_pickup_locations = (
    df["pickup_location"]
    .value_counts()
    .head(10)
)

print("\n10. TOP TEN PICKUP LOCATIONS")
print("-" * 50)

print(top_pickup_locations)


# ============================================================
# 15. TOP DROP LOCATIONS
# ============================================================

top_drop_locations = (
    df["drop_location"]
    .value_counts()
    .head(10)
)

print("\n11. TOP TEN DROP LOCATIONS")
print("-" * 50)

print(top_drop_locations)


# ============================================================
# 16. PAYMENT METHOD ANALYSIS
# ============================================================

payment_method_analysis = (
    completed_rides_df[
        "payment_method"
    ]
    .value_counts(dropna=False)
)

print("\n12. PAYMENT METHODS FOR COMPLETED RIDES")
print("-" * 50)

print(payment_method_analysis)


# ============================================================
# 17. RATING ANALYSIS
# ============================================================

average_customer_rating = (
    completed_rides_df[
        "customer_rating"
    ]
    .mean()
)

average_driver_rating = (
    completed_rides_df[
        "driver_ratings"
    ]
    .mean()
)

print("\n13. RATING ANALYSIS")
print("-" * 50)

print(
    "Average Customer Rating:",
    round(average_customer_rating, 2)
)

print(
    "Average Driver Rating:",
    round(average_driver_rating, 2)
)


# ============================================================
# 18. AUTOMATED BUSINESS INSIGHTS
# ============================================================

top_vehicle_by_revenue = (
    completed_vehicle_revenue
    .index[0]
)

top_vehicle_revenue = (
    completed_vehicle_revenue
    .iloc[0]["realized_revenue"]
)

top_vehicle_by_efficiency = (
    completed_vehicle_revenue[
        "average_revenue_per_km"
    ]
    .idxmax()
)

top_vehicle_efficiency = (
    completed_vehicle_revenue
    .loc[
        top_vehicle_by_efficiency,
        "average_revenue_per_km"
    ]
)

top_vehicle_by_completion = (
    vehicle_success
    .index[0]
)

top_vehicle_completion_rate = (
    vehicle_success
    .iloc[0]["completion_rate"]
)

print("\n14. KEY BUSINESS INSIGHTS")
print("-" * 50)

print(
    f"1. {completion_rate:.2f}% of all booking records "
    "were successfully completed."
)

print(
    f"2. Driver cancellations accounted for "
    f"{driver_cancellation_rate:.2f}% of all bookings "
    "and represented the largest unsuccessful category."
)

print(
    f"3. Peak booking demand occurred at "
    f"{highest_peak_hour}:00 with "
    f"{highest_peak_bookings:,} bookings."
)

print(
    f"4. {top_vehicle_by_revenue} generated the highest "
    f"realized revenue at approximately "
    f"₹{top_vehicle_revenue:,.2f}."
)

print(
    f"5. {top_vehicle_by_efficiency} generated the highest "
    f"average realized revenue per kilometre at "
    f"approximately ₹{top_vehicle_efficiency:.2f}/km."
)

print(
    f"6. {top_vehicle_by_completion} recorded the highest "
    f"ride completion rate at approximately "
    f"{top_vehicle_completion_rate:.2f}%."
)

print(
    "7. Repeated original Booking IDs should be treated "
    "as a data-governance risk because they represent "
    "different booking records."
)


# ============================================================
# 19. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("BUSINESS INSIGHT GENERATION COMPLETED SUCCESSFULLY")
print("=" * 70)