# Ola Ride Data Analytics

## Project Overview
This project analyzes 150,000 Ola ride booking records to understand booking performance, revenue trends, cancellations, vehicle performance, peak demand hours, and location-based ride patterns.

The complete workflow includes data cleaning, validation, feature engineering, exploratory data analysis, visualization, business insights, and an interactive Power BI dashboard.

## Tech Stack
- Python
- Pandas
- Matplotlib
- Power BI

## Dataset
- Total Records: 150,000
- Final Analytical Columns: 32
- Data includes booking status, vehicle type, pickup and drop locations, booking value, ride distance, ratings, payment methods, cancellation details, and engineered analytical features.

## Project Workflow

Raw Data  
↓  
Data Cleaning  
↓  
Data Validation  
↓  
Feature Engineering  
↓  
Exploratory Data Analysis  
↓  
Data Visualization  
↓  
Business Insights  
↓  
Power BI Dashboard  

## Key KPIs
- Total Bookings: 150,000
- Completed Rides: 93,000
- Completion Rate: 62%
- Total Revenue: ₹51.85M
- Average Booking Value: ₹508.30
- Failure Rate: 38%

## Key Business Insights
- 62% of total bookings were successfully completed.
- Driver cancellations were the largest cancellation category, accounting for 18% of total bookings.
- Peak ride demand occurred around 6 PM with approximately 12.4K bookings.
- Auto generated the highest total revenue at approximately ₹12.88M.
- Go Sedan had the highest average revenue per kilometer at approximately ₹38.22/km.
- Booking demand was distributed across multiple pickup and drop locations rather than being concentrated in one route.

## Dashboard

![Ola Ride Analytics Dashboard](images/ola_dashboard.png)

## Dashboard Features
- Interactive date filtering
- Vehicle type filtering
- Booking status filtering
- Payment method filtering
- Time-of-day analysis
- Pickup location filtering
- Booking status distribution
- Revenue by vehicle type
- Booking demand by hour
- Booking demand by day
- Top pickup and drop locations

## Repository Structure

```text
ola-ride-data-analytics/
│
├── data/
├── notebooks/
├── visualizations/
├── dashboard/
├── images/
├── README.md
└── requirements.txt