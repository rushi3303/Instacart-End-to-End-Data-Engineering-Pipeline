🚀 Instacart End-to-End Data Engineering Pipeline with Agentic AI

A production-style End-to-End Data Engineering and Agentic AI Platform built using the Instacart dataset.

This project combines a modern Data Engineering Pipeline based on the Medallion Architecture (Bronze → Silver → Gold) with an Agentic AI Multi-Agent System.

📌 Project Overview

Raw Instacart CSV files are processed through a complete ETL pipeline and transformed into analytics-ready datasets inside PostgreSQL.

Features

Raw Data Ingestion

Incremental Bronze Loading

Metadata-Based File Tracking

Data Cleaning and Validation

Bronze → Silver → Gold Transformation

SCD Type 1 and SCD Type 2

Audit Logging

Apache Airflow Orchestration

PostgreSQL Data Warehouse

Power BI Reporting

Agentic AI Multi-Agent System

Intent-Based Agent Routing

Pipeline Monitoring

Natural Language Data Interaction

Streamlit AI Interface

🏗️ System Architecture

Instacart CSV Files
        │
        ▼
Apache Airflow Scheduler
        │
        ▼
Python ETL Pipeline
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
PostgreSQL Data Warehouse
        │
        ├──► Power BI Dashboard
        │
        └──► Agentic AI System
                    │
                    ▼
               Intent Router
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
Pipeline Agent   Data Agent    Insight Agent
Support Agent    Action Agent  Report Agent
ML Agent

🤖 Agentic AI Architecture

The system uses a Multi-Agent Architecture.

User Question
      │
      ▼
Intent Router
      │
      ├── Pipeline Question ───► Pipeline Agent
      ├── Data Question ───────► Data Agent
      ├── Insight Question ────► Insight Agent
      ├── Recommendation ──────► Action Agent
      ├── Report Request ──────► Report Agent
      ├── Prediction Request ──► ML Agent
      └── Technical Question ──► Support Agent

🧠 AI Agents

The project contains 7 specialized AI agents.

#

Agent

Responsibility

1

⚙️ Pipeline Agent

Monitors pipeline status, Airflow DAG execution, latest run, failures and audit logs

2

🤝 Support Agent

Explains project architecture, technologies, Bronze, Silver, Gold and SCD concepts

3

📊 Data Agent

Handles questions related to products, orders, customers and PostgreSQL data

4

💡 Insight Agent

Generates business insights, trends and analytical observations

5

🎯 Action Agent

Provides business recommendations and suggested actions

6

📄 Report Agent

Generates project summaries and analytical reports

7

🧠 ML Agent

Handles prediction, forecasting and machine learning analysis

⚙️ Technology Stack

Category

Technologies

Programming Language

Python

Database

PostgreSQL

Workflow Orchestration

Apache Airflow

Containerization

Docker

Message Broker

Redis

Data Processing

Pandas

Database Toolkit

SQLAlchemy

Business Intelligence

Power BI

AI / LLM

Gemini

AI / ML

Hugging Face, Machine Learning

Agentic AI

Multi-Agent Architecture

Web Interface

Streamlit

Version Control

Git & GitHub

📂 Project Structure

Data_Engineering_project
│
├── agent/
│   ├── agents/
│   │   ├── pipeline_agent.py
│   │   ├── support_agent.py
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── action_agent.py
│   │   ├── report_agent.py
│   │   └── ml_agent.py
│   ├── tools/
│   │   ├── postgres_tool.py
│   │   └── airflow_tool.py
│   ├── router.py
│   └── main.py
│
├── airflow/
│   └── dags/
│       └── instacart_etl_dag.py
├── config/
├── data/source/csv/
├── scripts/
│   ├── load/
│   ├── transformation/
│   ├── audit/
│   ├── metadata/
│   ├── validation/
│   └── logging/
├── docker/
│   └── docker-compose.yml
├── images/
├── streamlit_app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

🥉 Bronze Layer

The Bronze Layer stores raw data from Instacart CSV files.

Features

Raw Data Storage

Chunk-Based CSV Loading

Dynamic Primary Key Detection

ON CONFLICT DO NOTHING

Metadata-Based Incremental Loading

File Timestamp Validation

File Size Validation

Skip Unchanged Files

Production Logging

🥈 Silver Layer

The Silver Layer performs:

Duplicate Removal

NULL Handling

Text Standardization

Data Transformation

Business Rule Validation

Data Quality Checks

🥇 Gold Layer

Business-ready analytical tables:

Product Dimension

Order Fact

Customer Summary

Sales Summary

🔄 SCD Implementation

SCD Type 1

Old records are overwritten when values change.

SCD Type 2

Historical changes are preserved by marking the old record inactive and inserting a new record.

📊 Metadata Framework

The Metadata Schema maintains:

File Name

Last Modified Timestamp

File Size

Last Loaded Timestamp

Load Status

This enables incremental processing and prevents unnecessary loading.

⚡ Incremental Loading Strategy

Read CSV Metadata
        │
        ▼
Compare File Information
        │
        ├── Last Modified Time
        └── File Size
                │
                ▼
          File Changed?
             │
        ┌────┴────┐
        │         │
       YES        NO
        │         │
        ▼         ▼
 Load File    Skip File

📋 Audit Framework

The Audit Layer tracks:

Pipeline Name

Layer Name

Table Name

Start Time

End Time

Execution Status

Execution Duration

Error Message

The Pipeline Agent uses these audit logs to monitor pipeline execution.

⚡ Apache Airflow Pipeline

Load to Bronze
        │
        ▼
Bronze to Silver
        │
        ▼
Silver to Gold
        │
        ▼
SCD Type 1
        │
        ▼
SCD Type 2

⚙️ Pipeline Agent Monitoring

The Pipeline Agent can answer:

What is the current pipeline status?

Is Airflow running?

When was the latest DAG run?

Are there any failed tasks?

It checks:

Airflow Server Status

DAG ID

Latest Pipeline Run

PostgreSQL Audit Logs

Successful Tasks

Failed Tasks

Running Tasks

💬 Example Questions

Pipeline Agent

What is the current pipeline status?
Is Airflow running?
When was the latest DAG run?
Show pipeline failures.

Support Agent

Explain Bronze, Silver and Gold layers.
What is SCD Type 2?
Explain the project architecture.
How does incremental loading work?

Data Agent

Show me top products.
Show customer data.
Show order information.
Show product details.

Insight Agent

Give me business insights from the data.
Analyze sales trends.
Show important trends.

Action Agent

What actions should we take to improve sales?
Give me business recommendations.
What should we do based on the data?

Report Agent

Generate a project summary report.
Create a full business report.
Generate an analytical report.

ML Agent

Predict future sales.
Give me a sales forecast.
Perform machine learning analysis.

🖥️ Streamlit AI Interface

Features:

Professional Chat Interface

7 AI Agents

Intent-Based Agent Routing

Pipeline Monitoring

Natural Language Questions

Data Visualizations

Voice Response

Light Mode

Dark Mode

Run:

streamlit run streamlit_app.py

🚀 Installation

1. Clone the Repository

git clone https://github.com/rushi3303/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME

2. Create Virtual Environment

python -m venv .venv

Activate on Windows:

.venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

🔐 Environment Variables

Create a .env file:

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

GEMINI_API_KEY=your_api_key

Do not upload the .env file to GitHub.

🐳 Run Docker Services

cd docker
docker compose up -d
docker compose ps

Stop services:

docker compose down

🌬️ Access Airflow

Open:

http://localhost:8080

DAG:

instacart_etl_pipeline

🤖 Run the Multi-Agent System

python -m agent.main

The Intent Router automatically selects the appropriate agent.

📊 Power BI Dashboard

The dashboard provides:

Sales Overview

Department Analysis

Customer Insights

Product Analysis

Order Trends

KPI Cards

Interactive Filters

🗄️ Database Schemas

Bronze

Silver

Gold

Metadata

Audit

🔐 .gitignore

.venv/
__pycache__/
.env
*.pyc
*.log
.vscode/
.idea/

📸 Project Screenshots

Add screenshots inside the images folder:

![Airflow DAG](images/airflow_dag.png)

![Docker Containers](images/docker_containers.png)

![PostgreSQL Schemas](images/postgres_schema.png)

![Power BI Dashboard](images/powerbi_dashboard.png)

![Agentic AI Interface](images/agentic_ai_interface.png)

🎯 Key Features

End-to-End Data Engineering Pipeline

Medallion Architecture

Bronze → Silver → Gold

Incremental Data Loading

Metadata-Based File Tracking

Data Cleaning and Validation

SCD Type 1

SCD Type 2

Audit Framework

Logging Framework

Apache Airflow Orchestration

Dockerized Deployment

PostgreSQL Data Warehouse

Power BI Dashboard

Agentic AI Integration

Multi-Agent Architecture

7 Specialized AI Agents

Intent-Based Routing

Pipeline Monitoring

Natural Language Data Interaction

Streamlit AI Interface

🚀 Future Enhancements

Real-Time Airflow REST API Monitoring

AWS S3 Integration

Azure Data Factory

Snowflake Data Warehouse

Apache Kafka Streaming

CI/CD Pipeline

Automated Data Quality Monitoring

Unit Testing

Email Alerts

Cloud Deployment

Advanced ML Models

RAG-Based Documentation Assistant

Role-Based Access Control

👨‍💻 Author

Rushikesh Sudam Bhosale

🎓 B.Tech – Electronics and Computer Engineering

GitHub: https://github.com/rushi3303

LinkedIn: https://www.linkedin.com/in/rushikeshbhosale
