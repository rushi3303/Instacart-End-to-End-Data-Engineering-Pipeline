# End-to-End Data Engineering Pipeline using PostgreSQL, Airflow & Power BI

## Project Overview

This project demonstrates an End-to-End Data Engineering Pipeline using the Instacart Dataset.

The pipeline loads raw CSV files into PostgreSQL, transforms the data through Bronze, Silver and Gold layers, automates ETL using Apache Airflow running on Docker, and visualizes business insights using Power BI.

---

## Project Architecture

```
CSV Files
    │
    ▼
Python ETL Scripts
    │
    ▼
Bronze Layer
    │
    ▼
Silver Layer
    │
    ▼
Gold Layer
    │
    ▼
Power BI Dashboard

Airflow
    │
    ▼
Automates Complete ETL Pipeline

Docker
    │
    ▼
Runs Airflow Services
```

---

## Technology Stack

- Python
- PostgreSQL
- Apache Airflow
- Docker
- Power BI
- SQLAlchemy
- Pandas
- Git & GitHub

---

## Project Structure

```
Data_Engineering_project/

│
├── airflow/
├── config/
├── data/
│   └── source/
│       └── csv/
│
├── docker/
├── scripts/
│   ├── load/
│   ├── transformation/
│   ├── metadata/
│   └── audit/
│
├── dashboard/
├── logs/
└── requirements.txt
```

---

## ETL Flow

### Bronze Layer

- Loads raw CSV files into PostgreSQL.
- Uses chunk processing for large files.
- Skip logic avoids reloading tables that already contain data.

---

### Silver Layer

- Cleans raw data.
- Removes unnecessary columns.
- Creates transformed tables.

---

### Gold Layer

- Creates business-ready tables.
- Used as the source for Power BI Dashboard.

---

## Airflow Pipeline

```
load_to_bronze
        │
        ▼
bronze_to_silver
        │
        ▼
silver_to_gold
```

The pipeline is executed automatically using Apache Airflow.

---

## Power BI Dashboard

Dashboard is connected to Gold Layer tables.

Dashboard provides:

- Sales Analysis
- Product Analysis
- Department Analysis
- KPI Cards
- Interactive Charts

---

## Features Implemented

- Bronze Layer
- Silver Layer
- Gold Layer
- Docker Setup
- Airflow DAG
- PostgreSQL Database
- Skip Logic for Bronze Loading
- Incremental Product Dimension Load
- Power BI Dashboard

---

## Future Enhancements

- Metadata Framework
- Audit Framework
- Full Incremental Loading
- Automatic Dashboard Refresh
- Environment Variables
- Logging Improvements

---

## Author

Rushikesh Sudam Bhosale

Data Engineering Internship Project