import pandas as pd
df=pd.read_csv(r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\ridebookings.csv")
print(df.shape)
print(df.columns.tolist())
cleaned_df=df.iloc[:,:21].copy()
print(cleaned_df.shape)
print(cleaned_df.head())
print(cleaned_df.info())
print(cleaned_df.describe(include="all"))
print(cleaned_df.isnull().sum())
print("duplicates rows",cleaned_df.duplicated().sum())
print(cleaned_df["Booking Status"].value_counts())
print()
print(cleaned_df["Vehicle Type"].value_counts())
print()
print(cleaned_df["Payment Method"].value_counts())
cleaned_df.columns=(
                   cleaned_df.columns.str.strip().str.lower().str.replace(" ","_")

)
print(cleaned_df.columns.tolist())

categorical_cols=[
    "booking_status",
    "vehicle_type",
    "pickup_location",
    "drop_location",
    "payment_method"
]
for col in categorical_cols:
    print(f"\n--- {col} ---")
    print(cleaned_df[col].value_counts(dropna=False))

missing = pd.DataFrame({
    "missing_count": cleaned_df.isnull().sum(),
    "missing_percentage": cleaned_df.isnull().mean() * 100
})

print(missing.sort_values("missing_percentage", ascending=False))

print(cleaned_df[cleaned_df["booking_value"] < 0])
print(cleaned_df[cleaned_df["ride_distance"] < 0])
print(cleaned_df[cleaned_df["driver_ratings"].notna() &
                 ((cleaned_df["driver_ratings"] < 1) |
                  (cleaned_df["driver_ratings"] > 5))])

cleaned_df.to_csv(
    r"C:\Users\hp\Desktop\ola_ride_dataAnalysis\data\raw\cleaned\ola_cleaned.csv",
    index=False
)
