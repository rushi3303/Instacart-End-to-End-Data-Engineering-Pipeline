# 🚀 Instacart End-to-End Data Engineering Pipeline

A production-style End-to-End Data Engineering Pipeline built using the Instacart Dataset following the **Medallion Architecture (Bronze → Silver → Gold)**. The project demonstrates scalable ETL processing, metadata-driven incremental loading, audit logging, Apache Airflow orchestration, PostgreSQL data warehousing, and Power BI reporting.

---

# 📌 Project Overview

This project simulates a real-world Data Engineering workflow by ingesting raw Instacart CSV files into PostgreSQL and transforming them into analytics-ready datasets.

The pipeline includes:

- Raw Data Ingestion
- Incremental Bronze Loading
- Metadata-Based File Tracking
- Data Cleaning & Validation
- Business Transformation
- Audit Logging
- Airflow Orchestration
- Power BI Reporting

---

# 🏗️ Architecture

```
                     Instacart CSV Files
                             │
                             ▼
                  Apache Airflow Scheduler
                             │
                             ▼
                  Python ETL Pipeline
                             │
        ┌──────────────────────────────────────┐
        │                                      │
        ▼                                      ▼
 Bronze Layer                           Metadata Layer
 (Raw Data)                          (File Tracking)
        │
        ▼
 Silver Layer
 (Clean & Validated Data)
        │
        ▼
 Gold Layer
 (Business Ready Tables)
        │
        ▼
 PostgreSQL Data Warehouse
        │
        ▼
      Power BI Dashboard
```

---

# ⚙️ Technology Stack

| Category | Technologies |
|----------|--------------|
| Language | Python |
| Database | PostgreSQL |
| Workflow Orchestration | Apache Airflow |
| Containerization | Docker |
| Message Broker | Redis |
| Data Processing | Pandas |
| ORM | SQLAlchemy |
| Reporting | Power BI |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```
Instacart-End-to-End-Data-Engineering-Pipeline

│
├── airflow/
│   └── dags/
│
├── config/
│
├── data/
│   └── source/
│       └── csv/
│
├── scripts/
│   ├── load/
│   ├── transformation/
│   ├── audit/
│   ├── metadata/
│   ├── validation/
│   └── logging/
│
├── docker/
│
├── images/
│
├── requirements.txt
│
└── README.md
```

---

# 🔄 ETL Workflow

```
CSV Files
    │
    ▼
Load to Bronze
    │
    ▼
Metadata Validation
(File Modified + File Size)
    │
    ▼
Skip Unchanged Files
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
```

---

# 🥉 Bronze Layer

### Features

- Raw Data Storage
- Chunk-based CSV Loading
- Dynamic Primary Key Detection
- ON CONFLICT DO NOTHING
- Metadata-based Incremental Loading
- File Timestamp Validation
- File Size Validation
- Skip Unchanged Files
- Production Logging

---

# 🥈 Silver Layer

### Features

- Data Cleaning
- Remove Duplicate Records
- NULL Handling
- Text Standardization
- Business Rule Validation
- Data Quality Checks

---

# 🥇 Gold Layer

Business-ready analytical tables:

- Product Dimension
- Order Fact
- Customer Summary
- Sales Summary

Optimized for BI reporting.

---

# 📊 Metadata Framework

Metadata Schema maintains:

- File Name
- Last Modified Timestamp
- File Size
- Last Loaded Timestamp
- Load Status

This enables incremental processing and prevents unnecessary data loading.

---

# 📋 Audit Framework

The Audit Layer tracks:

- Pipeline Name
- Layer Name
- Table Name
- Start Time
- End Time
- Execution Status
- Execution Duration

---

# ⚡ Incremental Loading Strategy

The Bronze Layer implements metadata-driven incremental loading.

### Workflow

```
Read CSV Metadata
        │
        ▼
Compare

Last Modified Time
+
File Size

        │
        ▼
File Changed?

     Yes ─────────► Load Bronze

     No ──────────► Skip File
```

Benefits

- Faster Execution
- Reduced Database Load
- No Duplicate Records
- Production-style Processing

---

# 🎯 Key Features

- Medallion Architecture
- Incremental Bronze Loading
- Metadata-driven File Tracking
- Skip Logic
- Dynamic Primary Key Detection
- Chunk-based Processing
- Audit Framework
- Data Validation
- Logging Framework
- Airflow DAG Orchestration
- Dockerized Deployment
- PostgreSQL Data Warehouse
- Power BI Dashboard

---

# 🗄️ Database Schemas

- Bronze
- Silver
- Gold
- Metadata
- Audit

---

# 🔄 Airflow Pipeline

```
Load to Bronze
        │
        ▼
Bronze to Silver
        │
        ▼
Silver to Gold
```

---

# 📈 Power BI Dashboard

The dashboard includes:

- Sales Overview
- Department Analysis
- Customer Insights
- Product Analysis
- Order Trends
- KPI Cards
- Interactive Filters

---

# 📸 Project Screenshots

## Airflow DAG

![Airflow DAG](images/airflow_dag.png)

---

## Docker Containers

![Docker](images/docker_containers.png)

---

## PostgreSQL Schemas

![PostgreSQL](images/postgres_schema.png)

---

## Power BI Dashboard

![Power BI](images/powerbi_dashboard.png)

---

# 🚀 Future Enhancements

- AWS S3 Integration
- Azure Data Factory
- Snowflake Data Warehouse
- Apache Kafka Streaming
- CI/CD Pipeline
- Data Quality Monitoring
- Unit Testing
- Email Alerts
- Cloud Deployment

---

# 👨‍💻 Author

**Rushikesh Sudam Bhosale**

**GitHub:** https://github.com/rushi3303

**LinkedIn:** https://www.linkedin.com/in/rushikeshbhosale