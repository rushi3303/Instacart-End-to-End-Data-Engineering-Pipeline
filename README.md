🚀 Instacart End-to-End Data Engineering Pipeline with Agentic AI

A production-style End-to-End Data Engineering and Agentic AI Platform built using the Instacart dataset.

This project combines a complete Data Engineering Pipeline based on the Medallion Architecture (Bronze → Silver → Gold) with a Multi-Agent Agentic AI System.

The raw Instacart dataset is ingested, validated, transformed, and stored in PostgreSQL through an automated ETL pipeline orchestrated using Apache Airflow.

On top of the data platform, an Agentic AI layer enables users to interact with the data and project using natural language.

The AI system uses Gemini LLM-based semantic intent routing to understand the user's question and automatically select the most suitable specialized AI agent.

📌 Table of Contents

Project Overview

Problem Statement

Project Objectives

Key Features

System Architecture

Data Engineering Workflow

Medallion Architecture

Bronze Layer

Silver Layer

Gold Layer

Incremental Loading

SCD Type 1 and Type 2

Metadata Framework

Audit Framework

Apache Airflow

PostgreSQL Data Warehouse

Agentic AI Architecture

AI Agents

LLM Intent Routing

RAG Knowledge System

ML Agent

Streamlit Application

Power BI Analytics

Project Structure

Technology Stack

Installation

Environment Variables

Running the Project

Example Questions

Complete End-to-End Flow

Business Value

Future Enhancements

Author

📊 Project Overview

The Instacart dataset contains information related to:

Orders

Order Products

Products

Departments

Aisles

Customer ordering behavior

Reorders

The project transforms this raw data into clean, validated, and analytics-ready datasets.

The complete platform follows:

Raw Instacart CSV
        ↓
Data Ingestion
        ↓
Bronze Layer
        ↓
Silver Layer
        ↓
Gold Layer
        ↓
PostgreSQL
        ↓
 ┌───────────────┬────────────────┐
 ↓               ↓                ↓
Power BI      Agentic AI       Analytics
                 ↓
             Gemini LLM
                 ↓
           Intent Router
                 ↓
        Specialized AI Agent

🎯 Problem Statement

Modern e-commerce platforms generate large amounts of customer, product, and order data.

Business and technical teams need answers to questions such as:

Which products are ordered most frequently?

Which customers are the most active?

What ordering patterns exist?

What is the current ETL pipeline status?

Are there failed pipeline tasks?

Are there data quality issues?

What is the demand level of a product?

What business actions should be taken?

Can a complete analytical report be generated automatically?

Traditional analytics systems require users to manually write SQL queries or navigate multiple dashboards.

This project provides a natural-language interface where users can ask questions and the Agentic AI system automatically determines how the question should be processed.

🎯 Project Objectives

The main objectives of this project are:

Build an End-to-End Data Engineering Pipeline.

Implement Medallion Architecture.

Ingest raw Instacart CSV data.

Store raw data in the Bronze Layer.

Clean and validate data in the Silver Layer.

Create business-ready Gold Layer tables.

Implement incremental loading.

Implement Metadata tracking.

Implement Audit logging.

Implement SCD Type 1 and SCD Type 2.

Orchestrate ETL using Apache Airflow.

Store analytical data in PostgreSQL.

Build Power BI analytics.

Build a Multi-Agent AI system.

Use Gemini LLM for semantic intent routing.

Implement RAG for project knowledge.

Integrate Machine Learning capabilities.

Provide a natural-language Streamlit interface.

⭐ Key Features

Data Engineering

Raw CSV ingestion

Chunk-based loading

Incremental loading

Metadata-based file tracking

Data cleaning

Data validation

Duplicate handling

NULL handling

Bronze → Silver → Gold transformation

SCD Type 1

SCD Type 2

Audit logging

Pipeline logging

PostgreSQL data warehouse

Apache Airflow orchestration

Docker environment

Agentic AI

Multi-Agent architecture

Gemini LLM

Semantic intent routing

7 specialized AI agents

Natural-language interaction

RAG knowledge retrieval

Business insight generation

Business recommendations

Automated report generation

Pipeline monitoring

ML-based analysis

Analytics

Customer analysis

Product analysis

Order analysis

Department analysis

Sales summaries

Customer summaries

Interactive visualizations

Power BI dashboards

CSV export

Audio briefing

🏗️ System Architecture

                         ┌──────────────────────┐
                         │  Instacart CSV Data  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Data Ingestion    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    BRONZE LAYER      │
                         │      Raw Data        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    SILVER LAYER      │
                         │ Cleaned & Validated  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     GOLD LAYER       │
                         │   Business Ready     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      PostgreSQL      │
                         │    Data Warehouse    │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┴─────────────────┐
                  │                                   │
                  ▼                                   ▼
          ┌────────────────┐                 ┌─────────────────┐
          │    Power BI    │                 │   Agentic AI    │
          │    Analytics   │                 │     System      │
          └────────────────┘                 └────────┬────────┘
                                                       │
                                                       ▼
                                                ┌──────────────┐
                                                │ Intent Router│
                                                │ Gemini LLM   │
                                                └──────┬───────┘
                                                       │
                  ┌──────────────┬──────────────┬──────┼──────────────┐
                  │              │              │      │              │
                  ▼              ▼              ▼      ▼              ▼
             Data Agent    Insight Agent   Pipeline  Support      Action
                                             Agent     Agent        Agent
                  │              │              │      │              │
                  └──────────────┴──────────────┴──────┴──────────────┘
                                                       │
                                          ┌────────────┴────────────┐
                                          │                         │
                                          ▼                         ▼
                                     Report Agent               ML Agent

🔄 Data Engineering Workflow

The ETL workflow follows:

Instacart CSV Files
        ↓
Apache Airflow
        ↓
Data Ingestion
        ↓
Bronze Layer
        ↓
Data Cleaning
        ↓
Silver Layer
        ↓
Transformations
        ↓
Gold Layer
        ↓
SCD Processing
        ↓
PostgreSQL
        ↓
Analytics + AI

🥉 Bronze Layer

The Bronze Layer stores the raw Instacart data.

The goal is to preserve source information before applying business transformations.

Bronze Features

Raw data storage

Chunk-based CSV loading

Dynamic primary-key detection

Duplicate protection

ON CONFLICT DO NOTHING

Metadata-based incremental loading

File timestamp validation

File size validation

Skip unchanged files

Logging

🥈 Silver Layer

The Silver Layer contains cleaned and validated data.

Main transformations include:

Duplicate removal

NULL handling

Data standardization

Text standardization

Data transformation

Business-rule validation

Data quality checks

The Silver Layer acts as the reliable foundation for Gold-layer processing.

🥇 Gold Layer

The Gold Layer contains business-ready analytical data.

Major analytical structures include:

Product Dimension

Contains product-level information used for product analytics.

Order Fact

Contains order-level analytical information.

Customer Summary

Contains aggregated customer ordering behavior.

Sales Summary

Contains summarized business information used for analytics and reporting.

The Gold Layer is consumed by:

Gold Layer
     ↓
PostgreSQL
     ↓
 ┌──────────────┬──────────────┐
 ↓              ↓              ↓
Power BI     Data Agent     Insight Agent

⚡ Incremental Loading

The project implements metadata-based incremental loading.

Instead of loading every CSV file during every execution, the system checks whether the source file has changed.

The system compares:

Last modified time

File size

Workflow:

Read CSV Metadata
       ↓
Compare File Information
       ↓
File Changed?
    /      \
  YES       NO
   ↓         ↓
Load File   Skip File

This prevents unnecessary processing of unchanged files.

🔄 SCD Type 1 and Type 2

SCD Type 1

SCD Type 1 overwrites an existing value when a change occurs.

Old Value
    ↓
Updated
    ↓
New Value

Historical values are not maintained.

SCD Type 2

SCD Type 2 preserves historical changes.

Existing Record
       ↓
Mark Old Record Inactive
       ↓
Insert New Record
       ↓
Historical Record Preserved

This allows historical dimension changes to be tracked.

📊 Metadata Framework

The Metadata Framework maintains information about source files.

Tracked information includes:

File Name

Last Modified Timestamp

File Size

Last Loaded Timestamp

Load Status

This framework enables incremental processing.

📋 Audit Framework

The Audit Framework records pipeline execution details.

Tracked information includes:

Pipeline Name

Layer Name

Table Name

Start Time

End Time

Execution Status

Execution Duration

Error Message

Rows Processed

Example:

Pipeline: Instacart_ETL
Layer: Silver
Table: orders
Status: Success
Rows Processed: 3421083

The Audit Framework is also used by the Pipeline Agent for pipeline monitoring.

🌬️ Apache Airflow

Apache Airflow is used to orchestrate the ETL pipeline.

The main DAG is:

instacart_etl_pipeline

The pipeline executes:

Load to Bronze
      ↓
Bronze to Silver
      ↓
Silver to Gold
      ↓
SCD Type 1
      ↓
SCD Type 2

Airflow provides:

DAG scheduling

Task execution

Task monitoring

Pipeline history

Failure tracking

Execution logs

🐳 Docker

Docker is used to provide a consistent environment for Airflow and supporting services.

Start services:

cd docker
docker compose up -d

Check services:

docker compose ps

Stop services:

docker compose down

🗄️ PostgreSQL Data Warehouse

PostgreSQL is used as the main data warehouse/database for the project.

The project separates data logically into:

Bronze
Silver
Gold
Metadata
Audit

PostgreSQL is used by the AI system for data-related questions.

Examples:

Top products
Customer summaries
Order analysis
Department analysis
Sales summaries
ETL audit history
Data quality

🤖 Agentic AI Architecture

The Agentic AI system contains 7 specialized AI agents.

The basic workflow is:

User Question
      ↓
Intent Router
      ↓
Gemini LLM
      ↓
Select Best Agent
      ↓
Specialized Agent
      ↓
Tool / Database / RAG / ML
      ↓
Result
      ↓
Final Response

The system decides which specialized agent should handle the question.

🧠 AI Agents

1. ⚙️ Pipeline Agent

Responsible for ETL and Airflow-related questions.

It can analyze:

Pipeline status

Airflow status

DAG execution

Latest pipeline run

Failed tasks

Successful tasks

Running tasks

Audit records

Example:

Is the ETL pipeline running successfully?

Workflow:

User Question
      ↓
Gemini Router
      ↓
Pipeline Agent
      ↓
Airflow / Audit Tool
      ↓
Pipeline Status
      ↓
Final Answer

2. 🤝 Support Agent

Responsible for project knowledge and technical explanations.

Examples:

What is the Bronze Layer?

Explain SCD Type 2.

How does incremental loading work?

Explain the project architecture.

The Support Agent uses the RAG system to retrieve relevant project knowledge.

3. 📊 Data Agent

Responsible for actual Instacart data analysis.

It handles questions related to:

Products

Orders

Customers

Departments

Aisles

Reorders

Counts

Aggregations

PostgreSQL data

Examples:

Show me the top 5 products.

Which customers have the highest order frequency?

Show department sales.

The Data Agent retrieves actual data from PostgreSQL.

4. 💡 Insight Agent

The Insight Agent generates business insights from actual data.

Workflow:

User Question
      ↓
Data Agent
      ↓
PostgreSQL
      ↓
Actual Data
      ↓
Insight Agent
      ↓
Gemini
      ↓
Business Insights

Example:

What patterns can you identify in customer ordering behavior?

The agent interprets the retrieved data and generates meaningful observations.

5. 🎯 Action Agent

The Action Agent generates recommended business actions.

Example:

What should we do to improve product availability?

Workflow:

User Question
      ↓
Action Agent
      ↓
Relevant Data
      ↓
Gemini
      ↓
Recommended Actions

Example recommendations may include:

Investigating high-demand products

Reviewing stock levels

Monitoring low reorder products

Improving supply planning

6. 📄 Report Agent

The Report Agent combines data, insights, and recommendations.

Workflow:

User Request
      ↓
Data Agent
      ↓
Actual Data
      ↓
Insight Agent
      ↓
Business Insights
      ↓
Action Agent
      ↓
Recommended Actions
      ↓
Complete Report

The generated report contains:

Title
Data
Insights
Recommended Actions

Example:

Create a summary report of the available data and insights.

7. 🧠 ML Agent

The ML Agent handles Machine Learning-related requests.

Current capabilities include:

Customer reorder prediction

Historical product demand analysis

Customer Reorder Prediction

The reorder model uses customer/order behavior features such as:

order_number
order_dow
order_hour_of_day
days_since_prior_order
add_to_cart_order

Example:

Predict whether this customer will reorder.

The model produces a prediction and reorder probability.

Product Demand Analysis

The ML Agent can analyze historical product ordering behavior.

Example:

What is the demand level of product 13176?

Example response:

Product ID: 13176
Historical Orders: 15480
Demand Level: High

This represents historical demand analysis rather than a full future time-series forecasting system.

🧠 LLM Intent Routing

The project uses Google Gemini as the Large Language Model.

Gemini is used to understand the semantic meaning of the user's question and select the appropriate agent.

Example:

User Question:

"What patterns can you identify in customer ordering behavior?"

Gemini understands that this requires business interpretation.

Therefore:

User Question
      ↓
Gemini Router
      ↓
Insight Agent

Another example:

"Is the ETL pipeline running successfully?"

The router identifies this as a pipeline monitoring request:

User Question
      ↓
Gemini Router
      ↓
Pipeline Agent

Another:

"What is the demand level of product 13176?"

The router identifies the ML/product-demand domain:

User Question
      ↓
Gemini Router
      ↓
ML Agent

The router is therefore based on semantic intent, not only exact keyword matching.

📚 RAG Knowledge System

The project includes a Retrieval-Augmented Generation system for project knowledge.

The RAG system contains components for:

Document loading

Text chunking

Embedding generation

Vector storage

Similarity search

Context retrieval

Main RAG components include:

document_loader.py
chunker.py
embedding_service.py
vector_store.py
build_index.py
index_manager.py
rag_engine.py

🔎 RAG Workflow

The indexing process is:

Project Documents
       ↓
Document Loader
       ↓
Text Chunking
       ↓
Embedding Model
       ↓
Vector Embeddings
       ↓
ChromaDB

When a user asks a question:

User Question
       ↓
Query Embedding
       ↓
Similarity Search
       ↓
Relevant Chunks
       ↓
Gemini LLM
       ↓
Final Answer

🧬 Embedding Model

The project uses Sentence Transformers for generating embeddings.

The embedding model is:

all-MiniLM-L6-v2

The model converts text into vector representations that can be compared using semantic similarity.

🗃️ ChromaDB

ChromaDB is used as the vector database.

The RAG system stores document embeddings and retrieves relevant information using similarity search.

The overall architecture is:

Documents
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
Gemini

🔗 Hybrid Knowledge Architecture

The project combines different knowledge sources depending on the question.

                    User Question
                          │
                          ▼
                    Gemini Router
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
      PostgreSQL         RAG               ML
          │               │                │
          ▼               ▼                ▼
      Data Agent      Support Agent     ML Agent
          │               │                │
          └───────────────┼────────────────┘
                          ▼
                     Final Answer

This creates a hybrid architecture combining:

LLM
+
RAG
+
SQL
+
Machine Learning
+
Multi-Agent System

🖥️ Streamlit Application

The project provides a Streamlit-based AI interface.

Run:

streamlit run streamlit_app.py

The interface supports:

Natural-language questions

AI agent routing

Agent execution status

Data records

Interactive visualizations

Business insights

Recommended actions

Pipeline diagnostics

Reports

CSV export

Voice query

Audio briefing

Dark mode interface

📊 Interactive Analytics

The Streamlit application can display query results using interactive visualizations.

Depending on the query and available data, the system can provide visual representations such as:

Bar charts

Product analysis charts

Sales visualizations

Customer analysis

Order frequency

The application can also export data as CSV.

📈 Power BI Analytics

The processed Gold-layer data can be used in Power BI.

The dashboard focuses on:

Executive Analytics

KPIs

Sales overview

Order overview

Product Analytics

Product performance

Product demand

Top products

Customer Analytics

Customer ordering behavior

Order frequency

Customer segmentation

Department Analytics

Department performance

Department sales

Product distribution

📂 Project Structure

Instacart-End-to-End-Data-Engineering-Pipeline/
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
│   │
│   ├── rag/
│   │   ├── documents/
│   │   ├── chroma_db/
│   │   ├── document_loader.py
│   │   ├── chunker.py
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   ├── build_index.py
│   │   ├── index_manager.py
│   │   └── rag_engine.py
│   │
│   ├── tools/
│   │   ├── postgres_tool.py
│   │   └── airflow_tool.py
│   │
│   ├── router.py
│   ├── main.py
│   └── gemini_service.py
│
├── airflow/
│   └── dags/
│       └── instacart_etl_dag.py
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
│   └── docker-compose.yml
│
├── ml/
│   ├── models/
│   │   └── reorder_model.pkl
│   ├── product_demand.py
│   └── train_reorder_model.py
│
├── sql/
│   └── constraints/
│
├── tests/
│
├── images/
│
├── streamlit_app.py
├── requirements.txt
├── requirements-local.txt
├── .gitignore
└── README.md

🛠️ Technology Stack

Category

Technology

Programming Language

Python

Data Processing

Pandas

Database

PostgreSQL

Database Toolkit

SQLAlchemy

ETL

Python

Orchestration

Apache Airflow

Containerization

Docker

Message Broker

Redis

Business Intelligence

Power BI

Web Interface

Streamlit

Visualization

Plotly

LLM

Google Gemini

Embeddings

Sentence Transformers

Embedding Model

all-MiniLM-L6-v2

Vector Database

ChromaDB

Machine Learning

Scikit-learn

Agentic AI

Multi-Agent Architecture

Version Control

Git

Repository

GitHub

🚀 Installation

1. Clone the Repository

git clone https://github.com/rushi3303/Instacart-End-to-End-Data-Engineering-Pipeline.git

cd Instacart-End-to-End-Data-Engineering-Pipeline

🐍 2. Create Virtual Environment

python -m venv .venv

Activate on Windows:

.venv\Scripts\activate

📦 3. Install Dependencies

pip install -r requirements.txt

For local development:

pip install -r requirements-local.txt

If required for the RAG/Agentic AI environment:

pip install google-genai chromadb sentence-transformers

🔐 Environment Variables

Create a local .env file.

Example:

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_database
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

GEMINI_API_KEY=your_gemini_api_key

⚠️ Important Security Rule

Never commit .env to GitHub.

Do not expose:

API Keys
Database Passwords
Credentials
Production Secrets

The .env file should remain local.

🐳 Run Docker

Go to the Docker directory:

cd docker

Start services:

docker compose up -d

Check running containers:

docker compose ps

Stop services:

docker compose down

🌬️ Access Airflow

Open:

http://localhost:8080

Main DAG:

instacart_etl_pipeline

🔄 Run ETL Pipeline

The Airflow pipeline follows:

Bronze
   ↓
Silver
   ↓
Gold
   ↓
SCD Type 1
   ↓
SCD Type 2

After execution, verify:

PostgreSQL
    ↓
Audit Records
    ↓
Pipeline Status

🤖 Run Agentic AI

From the project root:

python -m agent.main

The system will receive the user's question and route it to the appropriate specialized agent.

🖥️ Run Streamlit

From the project root:

streamlit run streamlit_app.py

The application will open in the browser.

💬 Example Questions

📊 Data Agent

Show me the top 5 products.

Which customers have the highest order frequency?

Show me customer order information.

Show department sales.

How many orders are there?

💡 Insight Agent

What patterns can you identify in customer ordering behavior?

What trends can you identify from the data?

What business insights can you generate?

⚙️ Pipeline Agent

Is the ETL pipeline running successfully?

What is the latest pipeline run?

Are there any failed tasks?

Show ETL audit history.

🤝 Support Agent

What is the Bronze Layer?

Explain the Medallion Architecture.

What is SCD Type 2?

How does incremental loading work?

🎯 Action Agent

What should we do to improve product availability?

What actions should we take to improve sales?

Give me business recommendations.

📄 Report Agent

Create a summary report of the available data and insights.

Generate a business report.

Create a complete analytical report.

🧠 ML Agent

What is the demand level of product 13176?

Show product demand analysis.

Predict whether this customer will reorder.

🔄 Complete End-to-End Flow

                 INSTACART DATA
                       │
                       ▼
               RAW CSV FILES
                       │
                       ▼
              APACHE AIRFLOW
                       │
                       ▼
               DATA INGESTION
                       │
                       ▼
              ┌────────────────┐
              │ BRONZE LAYER  │
              │   Raw Data    │
              └───────┬────────┘
                      │
                      ▼
              ┌────────────────┐
              │ SILVER LAYER  │
              │ Cleaned Data  │
              └───────┬────────┘
                      │
                      ▼
              ┌────────────────┐
              │  GOLD LAYER   │
              │ Business Data │
              └───────┬────────┘
                      │
                      ▼
                 POSTGRESQL
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
         POWER BI          AGENTIC AI
                                │
                                ▼
                           USER QUESTION
                                │
                                ▼
                         GEMINI LLM
                                │
                                ▼
                         INTENT ROUTER
                                │
       ┌────────┬────────┬─────┼─────┬────────┐
       ▼        ▼        ▼     ▼     ▼        ▼
      Data   Insight  Pipeline Support Action Report
      Agent   Agent    Agent   Agent  Agent  Agent
                                                   │
                                                   ▼
                                               ML Agent
                                │
                                ▼
                         RAG + SQL + ML
                                │
                                ▼
                    STREAMLIT AI COPILOT

🧠 How Agentic AI Works

The system works in five major stages.

Step 1 — User asks a question

Example:

What patterns can you identify in customer ordering behavior?

Step 2 — Intent Router

Gemini analyzes the semantic meaning of the question.

User Question
      ↓
Gemini
      ↓
Intent Classification

Step 3 — Specialized Agent

The router selects:

Insight Agent

Step 4 — Agent uses the required knowledge source

Depending on the agent:

Data Agent
    ↓
PostgreSQL

Support Agent
    ↓
RAG + ChromaDB

Pipeline Agent
    ↓
Airflow + Audit

ML Agent
    ↓
Machine Learning Model

Step 5 — Final Response

The result is returned to the Streamlit interface.

Agent Result
     ↓
Streamlit
     ↓
User

🔗 Hybrid AI Architecture

This project combines several modern technologies:

                ┌───────────────┐
                │   Gemini LLM  │
                └───────┬───────┘
                        │
                ┌───────▼───────┐
                │ Intent Router │
                └───────┬───────┘
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
       SQL             RAG               ML
        │               │                │
        ▼               ▼                ▼
   PostgreSQL        ChromaDB       ML Model
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                 Specialized Agent
                        │
                        ▼
                  Final Response

This makes the system a combination of:

LLM + RAG + SQL + ML + Multi-Agent AI + Data Engineering

💼 Business Value

This project demonstrates how Data Engineering and AI can work together.

For Data Engineers

Demonstrates:

ETL

ELT concepts

Medallion Architecture

Incremental loading

Data validation

Metadata management

Audit framework

SCD

PostgreSQL

Airflow

Docker

For Data Analysts

Demonstrates:

Customer analysis

Product analysis

Sales analysis

Order analysis

Power BI

Data visualization

Business insights

For AI / ML

Demonstrates:

Gemini LLM

Prompt-based intent routing

Multi-Agent architecture

RAG

Vector embeddings

ChromaDB

Machine Learning

For Business Users

Users can interact with the analytics platform using natural language instead of manually writing SQL queries.

🧪 Testing Workflow

Recommended testing sequence:

1. Start PostgreSQL
        ↓
2. Start Docker / Airflow
        ↓
3. Run ETL Pipeline
        ↓
4. Verify Bronze Layer
        ↓
5. Verify Silver Layer
        ↓
6. Verify Gold Layer
        ↓
7. Verify Audit Records
        ↓
8. Start Agentic AI
        ↓
9. Test all 7 Agents
        ↓
10. Start Streamlit
        ↓
11. Test Natural Language Queries

🔐 Git Security

The following should never be pushed to GitHub:

.env
.venv/
__pycache__/
*.pyc
*.log
.vscode/
.idea/

Recommended .gitignore:

.env
.venv/
__pycache__/
*.pyc
*.log
.vscode/
.idea/

📸 Project Screenshots

Recommended screenshots for the repository:

images/
│
├── airflow_dag.png
├── docker_containers.png
├── postgres_schema.png
├── powerbi_dashboard.png
└── agentic_ai_interface.png

Example:

![Airflow DAG](images/airflow_dag.png)

![PostgreSQL Schema](images/postgres_schema.png)

![Power BI Dashboard](images/powerbi_dashboard.png)

![Agentic AI Interface](images/agentic_ai_interface.png)

🚀 Future Enhancements

Possible future improvements include:

Real-time Airflow REST API monitoring

AWS S3 integration

Azure Data Factory integration

Snowflake integration

Apache Kafka streaming

CI/CD pipeline

Automated data quality monitoring

Email alerts

Cloud deployment

Advanced ML models

Advanced demand forecasting

RAG documentation improvements

Role-Based Access Control

Production monitoring

Automated testing

Model monitoring

Real-time analytics

🎓 Skills Demonstrated

This project demonstrates practical experience in:

Python
SQL
PostgreSQL
Pandas
SQLAlchemy
ETL
Data Cleaning
Data Validation
Medallion Architecture
Bronze / Silver / Gold
Incremental Loading
SCD Type 1
SCD Type 2
Metadata Framework
Audit Framework
Apache Airflow
Docker
Power BI
Machine Learning
Gemini LLM
Prompt Engineering
Intent Routing
RAG
Sentence Transformers
ChromaDB
Multi-Agent AI
Streamlit
Git
GitHub

👨‍💻 Author

Rushikesh Sudam Bhosale

B.Tech – Electronics and Computer Engineering

GitHub

https://github.com/rushi3303

LinkedIn

https://www.linkedin.com/in/rushikeshbhosale

⭐ Project Summary

             INSTACART DATA
                    │
                    ▼
           DATA ENGINEERING
                    │
                    ▼
        BRONZE → SILVER → GOLD
                    │
                    ▼
              POSTGRESQL
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
       POWER BI           AGENTIC AI
                                │
                                ▼
                           GEMINI LLM
                                │
                                ▼
                         INTENT ROUTER
                                │
       ┌────────┬────────┬─────┼─────┬────────┐
       ▼        ▼        ▼     ▼     ▼        ▼
      Data   Insight  Pipeline Support Action Report
      Agent   Agent    Agent   Agent  Agent  Agent
                                                   │
                                                   ▼
                                               ML Agent
                                │
                                ▼
                         RAG + SQL + ML
                                │
                                ▼
                    STREAMLIT AI COPILOT

🚀 Built With

Python • PostgreSQL • Apache Airflow • Docker • Power BI • Gemini • RAG • ChromaDB • Machine Learning • Streamlit • Multi-Agent AI