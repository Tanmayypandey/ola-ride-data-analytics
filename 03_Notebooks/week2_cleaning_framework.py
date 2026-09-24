from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "cleaned"
    / "ola_cleaned.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "week2_output"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "week2"
)

OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
REPORT_PATH.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

print("=" * 70)
print("OLA DATA COLLECTION AND CLEANING FRAMEWORK")
print("=" * 70)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{INPUT_FILE}"
    )

raw_df = pd.read_csv(
    INPUT_FILE,
    low_memory=False
)

df = raw_df.copy()

rows_before = len(df)
columns_before = len(df.columns)
duplicates_before = int(df.duplicated().sum())
missing_before = int(df.isna().sum().sum())

print("\nDataset loaded successfully.")
print("Rows:", f"{rows_before:,}")
print("Columns:", columns_before)
print("Missing values:", f"{missing_before:,}")
print("Exact duplicates:", f"{duplicates_before:,}")


# ============================================================
# 3. STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)


# ============================================================
# 4. CLEAN TEXT COLUMNS
# ============================================================

text_columns = df.select_dtypes(
    include="object"
).columns

for column in text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


# ============================================================
# 5. STANDARDIZE IMPORTANT CATEGORIES
# ============================================================

if "booking_status" in df.columns:
    status_mapping = {
        "completed": "Completed",
        "cancelled by customer": "Cancelled by Customer",
        "cancelled by driver": "Cancelled by Driver",
        "no driver found": "No Driver Found",
        "incomplete": "Incomplete"
    }

    df["booking_status"] = (
        df["booking_status"]
        .str.lower()
        .map(status_mapping)
        .fillna(df["booking_status"])
    )

if "vehicle_type" in df.columns:
    df["vehicle_type"] = (
        df["vehicle_type"]
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
        .replace({
            "Ebike": "eBike",
            "Uber Xl": "Uber XL"
        })
    )

if "payment_method" in df.columns:
    df["payment_method"] = (
        df["payment_method"]
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
        .replace({
            "Upi": "UPI",
            "Uber Wallet": "Uber Wallet"
        })
    )


# ============================================================
# 6. CONVERT DATE AND TIME
# ============================================================

date_failures = 0
time_failures = 0

if "date" in df.columns:
    original_date_non_null = int(
        df["date"].notna().sum()
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
        dayfirst=True
    )

    date_failures = (
        original_date_non_null
        - int(df["date"].notna().sum())
    )

if "time" in df.columns:
    original_time_non_null = int(
        df["time"].notna().sum()
    )

    converted_time = pd.to_datetime(
        df["time"],
        errors="coerce"
    )

    time_failures = (
        original_time_non_null
        - int(converted_time.notna().sum())
    )

    df["time"] = converted_time.dt.strftime(
        "%H:%M:%S"
    )


# ============================================================
# 7. NUMERIC CONVERSION
# ============================================================

numeric_columns = [
    "booking_value",
    "ride_distance",
    "avg_vtat",
    "avg_ctat",
    "driver_ratings",
    "customer_rating",
    "cancelled_rides_by_customer",
    "cancelled_rides_by_driver",
    "incomplete_rides"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# 8. MISSING-VALUE REPORT
# ============================================================

missing_report = pd.DataFrame({
    "column_name": df.columns,
    "missing_count": df.isna().sum().values,
    "missing_percentage": (
        df.isna().mean().values * 100
    ).round(2)
})

structural_columns = {
    "reason_for_cancelling_by_customer",
    "driver_cancellation_reason",
    "incomplete_rides_reason",
    "payment_method",
    "ride_distance",
    "driver_ratings",
    "customer_rating"
}

missing_report["classification"] = (
    missing_report["column_name"]
    .apply(
        lambda column:
        "Structural or status-dependent"
        if column in structural_columns
        else "Requires validation"
    )
)

missing_report["cleaning_action"] = (
    missing_report["classification"]
    .map({
        "Structural or status-dependent":
            "Preserve and validate by booking status",
        "Requires validation":
            "Review required-field rules"
    })
)

missing_report.to_csv(
    REPORT_PATH / "missing_value_report.csv",
    index=False
)


# ============================================================
# 9. STATUS-AWARE MISSING FLAGS
# ============================================================

completed_mask = (
    df["booking_status"].eq("Completed")
)

df["booking_value_missing_unexpected"] = (
    completed_mask
    & df["booking_value"].isna()
)

df["ride_distance_missing_unexpected"] = (
    completed_mask
    & df["ride_distance"].isna()
)

df["payment_method_missing_unexpected"] = (
    completed_mask
    & df["payment_method"].isna()
)

df["customer_cancel_reason_missing"] = (
    df["booking_status"].eq(
        "Cancelled by Customer"
    )
    & df[
        "reason_for_cancelling_by_customer"
    ].isna()
)

df["driver_cancel_reason_missing"] = (
    df["booking_status"].eq(
        "Cancelled by Driver"
    )
    & df[
        "driver_cancellation_reason"
    ].isna()
)

df["incomplete_reason_missing"] = (
    df["booking_status"].eq("Incomplete")
    & df["incomplete_rides_reason"].isna()
)


# ============================================================
# 10. EXACT DUPLICATES
# ============================================================

duplicate_records = df[
    df.duplicated(keep=False)
].copy()

duplicate_records.to_csv(
    REPORT_PATH / "exact_duplicate_records.csv",
    index=False
)

df = df.drop_duplicates().copy()


# ============================================================
# 11. UNIQUE ANALYTICAL RECORD ID
# ============================================================

if "booking_record_id" in df.columns:
    df = df.drop(
        columns=["booking_record_id"]
    )

df.insert(
    0,
    "booking_record_id",
    range(1, len(df) + 1)
)

duplicate_booking_ids = int(
    df["booking_id"].duplicated().sum()
)


# ============================================================
# 12. INVALID-VALUE CHECKS
# ============================================================

valid_statuses = {
    "Completed",
    "Cancelled by Customer",
    "Cancelled by Driver",
    "No Driver Found",
    "Incomplete"
}

df["invalid_booking_status"] = (
    ~df["booking_status"].isin(
        valid_statuses
    )
)

df["invalid_booking_value"] = (
    df["booking_value"].notna()
    & (df["booking_value"] < 0)
)

df["invalid_ride_distance"] = (
    df["ride_distance"].notna()
    & (df["ride_distance"] < 0)
)

df["invalid_driver_rating"] = (
    df["driver_ratings"].notna()
    & ~df["driver_ratings"].between(1, 5)
)

df["invalid_customer_rating"] = (
    df["customer_rating"].notna()
    & ~df["customer_rating"].between(1, 5)
)

invalid_columns = [
    "invalid_booking_status",
    "invalid_booking_value",
    "invalid_ride_distance",
    "invalid_driver_rating",
    "invalid_customer_rating"
]

invalid_mask = df[invalid_columns].any(
    axis=1
)

invalid_records = df[
    invalid_mask
].copy()

invalid_records.to_csv(
    REPORT_PATH / "invalid_records.csv",
    index=False
)


# ============================================================
# 13. REVENUE PER KM
# ============================================================

df["revenue_per_km"] = np.where(
    (
        df["booking_value"].notna()
        & df["ride_distance"].notna()
        & (df["ride_distance"] > 0)
    ),
    df["booking_value"]
    / df["ride_distance"],
    np.nan
)


# ============================================================
# 14. IQR OUTLIER DETECTION
# ============================================================

outlier_columns = [
    "booking_value",
    "ride_distance",
    "avg_vtat",
    "avg_ctat",
    "revenue_per_km"
]

outlier_results = []

for column in outlier_columns:

    if column not in df.columns:
        continue

    valid_values = df[column].dropna()

    q1 = valid_values.quantile(0.25)
    q3 = valid_values.quantile(0.75)
    iqr = q3 - q1

    lower_limit = q1 - (1.5 * iqr)
    upper_limit = q3 + (1.5 * iqr)

    flag_column = f"{column}_outlier"

    df[flag_column] = (
        (df[column] < lower_limit)
        | (df[column] > upper_limit)
    )

    outlier_count = int(
        df[flag_column].sum()
    )

    outlier_results.append({
        "column_name": column,
        "q1": round(q1, 2),
        "q3": round(q3, 2),
        "iqr": round(iqr, 2),
        "lower_limit": round(
            lower_limit,
            2
        ),
        "upper_limit": round(
            upper_limit,
            2
        ),
        "outlier_count": outlier_count,
        "outlier_percentage": round(
            outlier_count / len(df) * 100,
            2
        ),
        "treatment": (
            "Flagged for review; not deleted"
        )
    })

outlier_report = pd.DataFrame(
    outlier_results
)

outlier_report.to_csv(
    REPORT_PATH / "outlier_report.csv",
    index=False
)

outlier_flag_columns = [
    column
    for column in df.columns
    if column.endswith("_outlier")
]

outlier_mask = df[
    outlier_flag_columns
].any(axis=1)

df[outlier_mask].to_csv(
    REPORT_PATH / "outlier_records.csv",
    index=False
)


# ============================================================
# 15. FEATURE ENGINEERING
# ============================================================

if "date" in df.columns:
    df["booking_year"] = (
        df["date"].dt.year
    )
    df["booking_month"] = (
        df["date"].dt.month
    )
    df["booking_day"] = (
        df["date"].dt.day
    )
    df["booking_day_name"] = (
        df["date"].dt.day_name()
    )
    df["is_weekend"] = (
        df["date"].dt.dayofweek >= 5
    ).astype(int)

if "time" in df.columns:
    df["booking_hour"] = pd.to_numeric(
        df["time"].str[:2],
        errors="coerce"
    )

df["is_completed"] = (
    df["booking_status"].eq("Completed")
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
    df["booking_status"].eq("Incomplete")
).astype(int)


# ============================================================
# 16. QUALITY METRICS
# ============================================================

rows_after = len(df)
duplicates_after = int(
    df.duplicated().sum()
)

required_columns = [
    "date",
    "time",
    "booking_id",
    "booking_status",
    "customer_id",
    "vehicle_type",
    "pickup_location",
    "drop_location"
]

required_values = (
    len(df) * len(required_columns)
)

available_required_values = int(
    df[required_columns]
    .notna()
    .sum()
    .sum()
)

required_completeness = (
    available_required_values
    / required_values
    * 100
)

invalid_count = int(
    invalid_mask.sum()
)

validity_rate = (
    1 - invalid_count / len(df)
) * 100

unique_record_rate = (
    df["booking_record_id"].nunique()
    / len(df)
    * 100
)

quality_score = np.mean([
    required_completeness,
    validity_rate,
    unique_record_rate
])

quality_scorecard = pd.DataFrame([
    {
        "metric": "Required-field completeness rate",
        "score_percentage": round(
            required_completeness,
            2
        )
    },
    {
        "metric": "Validity rate",
        "score_percentage": round(
            validity_rate,
            2
        )
    },
    {
        "metric": "Unique analytical record rate",
        "score_percentage": round(
            unique_record_rate,
            2
        )
    },
    {
        "metric": "Overall data-quality score",
        "score_percentage": round(
            quality_score,
            2
        )
    }
])

quality_scorecard.to_csv(
    REPORT_PATH / "data_quality_scorecard.csv",
    index=False
)


# ============================================================
# 17. BEFORE-AFTER COMPARISON
# ============================================================

comparison = pd.DataFrame([
    {
        "metric": "Rows",
        "before_cleaning": rows_before,
        "after_cleaning": rows_after,
        "action": "Removed confirmed exact duplicates only"
    },
    {
        "metric": "Exact duplicate rows",
        "before_cleaning": duplicates_before,
        "after_cleaning": duplicates_after,
        "action": "Exact duplicate removal"
    },
    {
        "metric": "Missing values",
        "before_cleaning": missing_before,
        "after_cleaning": int(
            df.isna().sum().sum()
        ),
        "action": (
            "Structural values preserved and "
            "unexpected values flagged"
        )
    },
    {
        "metric": "Duplicate original booking IDs",
        "before_cleaning": duplicate_booking_ids,
        "after_cleaning": duplicate_booking_ids,
        "action": (
            "Preserved and unique analytical "
            "record ID created"
        )
    },
    {
        "metric": "Invalid records",
        "before_cleaning": invalid_count,
        "after_cleaning": invalid_count,
        "action": (
            "Flagged for review instead of "
            "silent deletion"
        )
    }
])

comparison.to_csv(
    REPORT_PATH / "before_after_comparison.csv",
    index=False
)


# ============================================================
# 18. SAVE FINAL DATASET
# ============================================================

output_file = (
    OUTPUT_PATH
    / "ola_week2_analysis_ready.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# 19. REPORT-READY SUMMARY
# ============================================================

summary_text = f"""
OLA DATA COLLECTION AND CLEANING FRAMEWORK
Generated: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

DATA SOURCE
Source file: {INPUT_FILE.name}
Collection method: Existing CSV dataset from Ola Ride Data Analytics project.

DATASET SIZE
Rows before cleaning: {rows_before:,}
Rows after cleaning: {rows_after:,}
Columns before cleaning: {columns_before}
Columns after framework implementation: {len(df.columns)}

DATA QUALITY FINDINGS
Missing values before cleaning: {missing_before:,}
Exact duplicates before cleaning: {duplicates_before:,}
Exact duplicates after cleaning: {duplicates_after:,}
Repeated original booking IDs: {duplicate_booking_ids:,}
Invalid records flagged: {invalid_count:,}
Outlier records flagged: {int(outlier_mask.sum()):,}
Date conversion failures: {date_failures:,}
Time conversion failures: {time_failures:,}

QUALITY SCORES
Required-field completeness: {required_completeness:.2f}%
Validity rate: {validity_rate:.2f}%
Unique analytical record rate: {unique_record_rate:.2f}%
Overall data-quality score: {quality_score:.2f}%

CLEANING DECISIONS
1. Structural missing values were preserved.
2. Unexpected missing values were flagged by booking status.
3. Exact duplicate rows were removed.
4. Repeated booking IDs were preserved because they may represent separate analytical observations.
5. A unique booking_record_id was created.
6. Invalid values were flagged for review.
7. IQR outliers were flagged but not automatically deleted.
8. Original project datasets and Power BI files were not modified.

RISK CONTROLS
- Raw and existing analytical files remain unchanged.
- Week 2 output is stored separately.
- Status-aware missing-value checks prevent incorrect imputation.
- Unique analytical IDs reduce double-counting risk.
- Invalid-value flags protect rating and revenue analysis.
- Outlier flags prevent accidental deletion of genuine high-value rides.
- Customer identifiers should not be shown in public reports.

FINAL OUTPUT
{output_file}
"""

summary_file = (
    REPORT_PATH
    / "report_ready_findings.txt"
)

summary_file.write_text(
    summary_text.strip(),
    encoding="utf-8"
)


# ============================================================
# 20. FINAL OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("FRAMEWORK COMPLETED SUCCESSFULLY")
print("=" * 70)

print("Rows before:", f"{rows_before:,}")
print("Rows after:", f"{rows_after:,}")
print("Repeated booking IDs:", f"{duplicate_booking_ids:,}")
print("Invalid records:", f"{invalid_count:,}")
print("Outlier records:", f"{int(outlier_mask.sum()):,}")
print("Quality score:", f"{quality_score:.2f}%")

print("\nFinal dataset:")
print(output_file)

print("\nEvidence reports:")
print(REPORT_PATH)

print("\nReport-ready findings:")
print(summary_file)