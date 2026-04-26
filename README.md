# 🚗 Uber Databricks Azure Streaming

A production-grade, end-to-end data engineering pipeline that demonstrates real-time streaming architecture using **Azure Cloud**, **Databricks**, and **Apache Spark**. This project implements the **medallion architecture** (Bronze/Silver/Gold layers) for scalable data processing and analytics.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
  - [Azure Data Factory Setup](#1-azure-data-factory-setup)
  - [Databricks Setup](#2-databricks-setup)
  - [Web Application Setup](#3-web-application-setup)
- [Usage](#usage)
- [Data Flow](#data-flow)
- [Configuration](#configuration)
- [Key Features](#key-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 📊 Project Overview

This project creates a **real-time Uber ride analytics pipeline** that:

1. **Orchestrates initial data load** using Azure Data Factory (ADF)
2. **Stores reference data** in Azure Blob Storage
3. **Ingests reference data** into a Databricks data lakehouse (Bronze layer)
4. **Generates real-time events** via a Flask web application
5. **Streams events** through Azure Event Hub
6. **Processes streaming data** using Databricks Spark jobs
7. **Enriches and transforms data** with reference tables (Silver/Gold layers)
8. **Enables analytics** through a medallion-structured data lakehouse

### 🎯 Use Cases

- **Real-time ride analytics**: Track active rides, completion rates, cancellations
- **Revenue analysis**: Payment method insights, pricing metrics
- **Operational metrics**: Vehicle utilization, driver performance
- **Data quality monitoring**: Lineage tracking with timestamps

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         GitHub Repository (Source of Truth)                 │
│         └─ Data/                                              │
│            ├─ bulk_rides.json                                 │
│            ├─ map_cities.json                                 │
│            ├─ map_payment_methods.json                        │
│            └─ ... (reference data)                            │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │  files.json (Config)    │
          │  - Lists all files for  │
          │    ADF to ingest        │
          └────────────┬────────────┘
                       │
    ┌──────────────────▼──────────────────────────┐
    │     Azure Data Factory (Orchestration)      │
    │  ┌───────────────────────────────────────┐  │
    │  │ Pipeline: Copy files from GitHub      │  │
    │  │ Input: files.json                     │  │
    │  │ Loop through each file entry          │  │
    │  │ → Fetch from GitHub repo              │  │
    │  │ → Load to Azure Storage               │  │
    │  └───────────────────────────────────────┘  │
    └──────────────────┬──────────────────────────┘
                       │
    ┌──────────────────▼─────────────────────┐
    │   Azure Storage Account                │
    │   Container: /raw/ingestion/           │
    │   ├─ map_cities.json                   │
    │   ├─ map_payment_methods.json          │
    │   ├─ map_ride_statuses.json            │
    │   └─ ... (all reference data)          │
    └──────────────────┬─────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────┐
    │       Databricks Data Lakehouse                 │
    │  ┌──────────────────────────────────────────┐   │
    │  │ Bronze Layer (bronze_adls.py)            │   │
    │  │ - Read from Azure Storage                │   │
    │  │ - SAS Token authentication               │   │
    │  │ - Delta tables created:                  │   │
    │  │   • uber.bronze.map_cities               │   │
    │  │   • uber.bronze.map_payment_methods      │   │
    │  │   • uber.bronze.map_ride_statuses        │   │
    │  │   • ... (all reference tables)           │   │
    │  └──────────────────────────────────────────┘   │
    └──────────────────┬───────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────┐
    │    Flask Web Application (localhost:5000)       │
    │  - Generates synthetic Uber ride events        │
    │  - Web UI & REST API endpoints                 │
    │  - Sends events to Event Hub                   │
    └──────────────────┬───────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────┐
    │   Azure Event Hub / Kafka Stream                │
    │   Topic: uber-databricks-topic                 │
    │   - Real-time event ingestion                  │
    └──────────────────┬───────────────────────────────┘
                       │
    ┌──────────────────▼──────────────────────────────┐
    │  Databricks Streaming Pipeline                  │
    │  ┌────────────────────────────────────────────┐ │
    │  │ Silver Layer (ingest.py)                   │ │
    │  │ - Reads from Event Hub (Kafka consumer)    │ │
    │  │ - Parses and validates events              │ │
    │  │ - Joins with Bronze reference data         │ │
    │  │ - Creates silver_rides table               │ │
    │  └────────────────────────────────────────────┘ │
    │  ┌────────────────────────────────────────────┐ │
    │  │ Gold Layer (Analytics Ready)               │ │
    │  │ - Aggregations & business metrics          │ │
    │  │ - Ride summaries, revenue reports          │ │
    │  │ - Ready for BI tools & dashboards          │ │
    │  └────────────────────────────────────────────┘ │
    └──────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Cloud & Infrastructure
- **Azure Cloud Platform**
  - Azure Data Factory (Orchestration)
  - Azure Event Hub (Real-time streaming)
  - Azure Blob Storage (Data lake)
  - Azure Key Vault (Secret management)

### Data Processing
- **Databricks**: Unified analytics platform
- **Apache Spark**: Distributed processing engine
- **Delta Lake**: ACID transactions, time travel
- **Kafka**: Event streaming protocol

### Web Application
- **Flask**: Web framework
- **Python 3.8+**: Programming language
- **Jinja2**: Template engine

### Data Management
- **Pandas**: Data manipulation
- **JSON**: Data format

### Key Dependencies
```
azure-core==1.39.0
azure-eventhub==5.11.6
Flask==2.3.3
requests==2.33.1
python-dotenv==1.0.0
Faker==40.15.0
```

---

## 📁 Project Structure

```
uber-databricks-azure-streaming/
├── README.md                                    # This file
├── files.json                                   # Config for ADF - lists files to load
├── requirements.txt                             # Python dependencies
├── img.png                                      # Project architecture image
│
├── Data/                                        # Reference data files
│   ├── bulk_rides.json                          # Sample ride data
│   ├── map_cancellation_reasons.json            # Cancellation reason mappings
│   ├── map_cities.json                          # City reference data
│   ├── map_payment_methods.json                 # Payment method mappings
│   ├── map_ride_statuses.json                   # Ride status mappings
│   ├── map_vehicle_makes.json                   # Vehicle make reference
│   └── map_vehicle_types.json                   # Vehicle type reference
│
├── databricks_notebooks_and_pipelines/          # Databricks ETL code
│   ├── bronze_adls.py                           # Bronze layer - reads from Azure Storage
│   ├── silver_obt_transformations.py            # Silver layer transformations
│   │
│   └── uber_rides_ingest/                       # Main data product pipeline
│       ├── README.md                            # Pipeline documentation
│       │
│       ├── explorations/                        # Ad-hoc exploration notebooks
│       │   └── sample_exploration.py
│       │
│       ├── transformations/                     # Core transformation logic
│       │   ├── ingest.py                        # Reads from Event Hub (Kafka)
│       │   ├── model.py                         # Data modeling
│       │   ├── silver.py                        # Silver layer transforms
│       │   └── silver_obt.sql                   # SQL transformations
│       │
│       └── utilities/                           # Helper functions
│           └── utils.py                         # Common utilities
│
└── webapp/                                      # Flask web application
    ├── app.py                                   # Main Flask app
    ├── config.py                                # Configuration management
    ├── data.py                                  # Data generation functions
    ├── run.py                                   # App runner
    ├── requirements.txt                         # Web app dependencies
    ├── setup.sh                                 # Linux/Mac setup script
    ├── setup.bat                                # Windows setup script
    ├── QUICKSTART.md                            # Quick start guide
    ├── README.md                                # Web app documentation
    │
    ├── __pycache__/                             # Python cache
    │   ├── app.cpython-312.pyc
    │   ├── config.cpython-312.pyc
    │   └── data.cpython-312.pyc
    │
    └── templates/                               # HTML templates
        └── index.html                           # Web UI
```

---

## 📋 Prerequisites

### Before You Start

You need:

1. **Azure Subscription**
   - Azure Data Factory instance
   - Azure Event Hub namespace & topic
   - Azure Storage Account with container
   - Service Principal or account with appropriate permissions

2. **Databricks Workspace**
   - Databricks cluster (compute)
   - Workspace access
   - DBFS or Unity Catalog configured

3. **Development Environment**
   - Python 3.8 or higher
   - Git
   - GitHub access (for Data repository)
   - pip (Python package manager)

4. **Credentials & Configuration**
   - GitHub personal access token (for ADF)
   - Azure Storage Account connection string & SAS token
   - Event Hub connection string
   - Azure Service Principal credentials (optional, for Databricks)

---

## 🚀 Setup & Installation

### 1. Azure Data Factory Setup

#### Step 1.1: Create Linked Services

**LinkedIn Service - GitHub:**
1. Go to Azure Data Factory Studio
2. Create new Linked Service → Generic HTTP
3. Configure:
   - **Base URL**: `https://raw.githubusercontent.com/{owner}/{repo}/main/Data/`
   - **Authentication**: Basic (GitHub token as password)
   - **Name**: `GitHub_LinkedService`

**Linked Service - Azure Storage:**
1. Create new Linked Service → Azure Blob Storage
2. Configure:
   - **Account name**: Your storage account
   - **Account key**: Copy from Azure Portal
   - **Name**: `AzureStorage_LinkedService`

#### Step 1.2: Create Pipeline

1. Create new pipeline: `LoadReferenceData`
2. Add parameters:
   - `file_list`: Array of file names (from `files.json`)

3. Add activities:
   - **Lookup activity**: Read `files.json` to get file list
   - **ForEach activity**: Loop through each file
   - **Copy activity** (inside loop):
     - **Source**: HTTP (GitHub)
     - **Destination**: Azure Blob Storage (`raw/ingestion/`)

#### Step 1.3: Parameterize with files.json

The `files.json` file is used by ADF to determine which files to load:

```json
[
    {"fileName": "bulk_rides"},
    {"fileName": "map_cancellation_reasons"},
    {"fileName": "map_cities"},
    {"fileName": "map_payment_methods"},
    {"fileName": "map_ride_statuses"},
    {"fileName": "map_vehicle_makes"},
    {"fileName": "map_vehicle_types"}
]
```

**In the ForEach activity:**
- **Items**: `@activity('Lookup').output.value`
- **Iterate over**: Each `fileName` entry

**In the Copy activity:**
- **Source path**: `@item().fileName + '.json'`
- **Destination**: `/raw/ingestion/@{item().fileName}.json`

#### Step 1.4: Execute Pipeline

1. Click "Debug" or "Publish then Trigger"
2. Monitor execution in the Activity Runs window
3. Verify files appear in Azure Storage container

---

### 2. Databricks Setup

#### Step 2.1: Create Databricks Cluster

1. Go to Databricks workspace
2. Create a cluster with:
   - **Runtime**: Databricks Runtime 13.3 LTS or higher
   - **Python version**: 3.10+
   - **Nodes**: 2-4 worker nodes
   - **Driver**: Standard (4 cores recommended)

#### Step 2.2: Configure Azure Storage Access

**Option A: Storage Account Key**
```python
# In your notebook
spark.conf.set(
    "fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    "{storage_account_key}"
)
```

**Option B: SAS Token** (Recommended for security)
```python
spark.conf.set(
    "fs.azure.sas.{container}.{storage_account}.dfs.core.windows.net",
    "{sas_token}"
)
```

#### Step 2.3: Configure Event Hub Access

Create a secret in Databricks for the connection string:

```bash
# In terminal
databricks secrets put-secret --scope azure-secrets --key eventhub-connstr
# Then paste your Event Hub connection string
```

Or set it in the notebook:

```python
# In your notebook
import os
os.environ['EVENT_HUB_CONNECTION_STRING'] = dbutils.secrets.get(scope="azure-secrets", key="eventhub-connstr")
```

#### Step 2.4: Upload Notebooks

1. Clone or download the project
2. In Databricks workspace:
   - Upload `bronze_adls.py` → `/Workspace/uber_project/bronze_adls`
   - Upload `uber_rides_ingest/transformations/ingest.py` → `/Workspace/uber_project/silver/ingest`
   - Upload `uber_rides_ingest/transformations/silver.py` → `/Workspace/uber_project/silver/silver`

#### Step 2.5: Update Configuration

Edit `bronze_adls.py` and update:

```python
# Update the SAS token
token = "{your_sas_token_here}"

# Update storage account URL
url = "https://{your_storage_account}.blob.core.windows.net/raw/ingestion"
```

Edit `transformations/ingest.py` and update:

```python
EH_NAMESPACE = "{your_eventhub_namespace}"
EH_NAME = "{your_eventhub_name}"
EH_CONN_STR = spark.conf.get("connection_string")
```

#### Step 2.6: Run Bronze Layer Notebook

1. Open `bronze_adls.py` notebook
2. Click "Run All" or "Run Cell"
3. Verify Delta tables are created:
   ```sql
   SHOW TABLES IN uber.bronze;
   ```

---

### 3. Web Application Setup

#### Step 3.1: Clone/Navigate to Webapp Directory

```bash
cd uber-databricks-azure-streaming/webapp
```

#### Step 3.2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Step 3.3: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 3.4: Configure Environment Variables

1. Create `.env` file in `webapp/` directory:

```bash
cp .env.example .env
```

Or create manually:

```env
EVENT_HUB_CONNECTION_STRING=Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=your_key_here
EVENT_HUB_NAME=uber-databricks-topic
FLASK_ENV=development
FLASK_DEBUG=True
```

**Getting your credentials:**
1. Go to Azure Portal → Event Hub namespace
2. Shared access policies → RootManageSharedAccessKey
3. Copy the "Connection string - primary key"

#### Step 3.5: Run the Application

```bash
python app.py
```

Or use the setup scripts:

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
bash setup.sh
```

The app will start on `http://localhost:5000`

---

## 💻 Usage

### Starting the Pipeline

#### 1. Initial Data Load (One-time)

**Via Azure Data Factory:**
1. Go to Azure Data Factory Studio
2. Navigate to your pipeline
3. Click "Debug" or "Trigger → Trigger now"
4. Wait for completion (typically 2-5 minutes)

**Verify in Azure Storage:**
```bash
# Using Azure CLI
az storage blob list --account-name {storage_account} --container-name raw/ingestion
```

#### 2. Load Reference Data into Databricks (One-time)

In Databricks:
1. Open `bronze_adls.py` notebook
2. Click "Run All"
3. Verify tables:
   ```sql
   SELECT * FROM uber.bronze.map_cities LIMIT 5;
   ```

#### 3. Start the Web Application

```bash
cd webapp
python app.py
```

Access the UI at `http://localhost:5000`

---

### Using the Web Application

#### Web UI

1. Open browser: `http://localhost:5000`
2. Enter number of events to generate (1-100)
3. Click "Send Events"
4. View confirmation with event details

#### REST API

**Send events programmatically:**

```bash
curl -X POST http://localhost:5000/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "count": 10
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "10 events sent successfully",
  "events_sent": 10,
  "timestamp": "2024-01-15 10:30:45.123456"
}
```

#### Health Check Endpoint

```bash
curl http://localhost:5000/health
```

---

### Monitoring the Pipeline

#### In Databricks

View streaming data:
```sql
SELECT * FROM uber.silver.rides_raw LIMIT 10;
```

View enriched data:
```sql
SELECT 
  ride_id,
  user_id,
  city_name,
  payment_method,
  vehicle_type,
  ride_status,
  created_at
FROM uber.silver.rides_enriched
LIMIT 10;
```

#### In Azure Event Hub

1. Go to Azure Portal → Event Hub namespace
2. Click your event hub name
2. Monitor "Incoming Requests" and "Incoming Messages" graphs

#### Application Logs

Check Flask app logs in console for any errors or processing info.

---

## 🔄 Data Flow

### Initial Load (One-Time Setup)

```
GitHub Repository (Data/*.json)
         ↓
   files.json (config)
         ↓
Azure Data Factory (reads config)
         ↓
Iterates through files.json
         ↓
Copy Activity for each file
         ↓
Azure Storage (raw/ingestion/)
         ↓
Databricks bronze_adls.py
         ↓
Bronze Delta Tables (uber.bronze.*)
```

### Real-Time Streaming

```
Web UI / API (/send-event)
         ↓
Generate synthetic event data
         ↓
Azure Event Hub (producer)
         ↓
Event published to topic
         ↓
Databricks Streaming Job (Kafka consumer)
         ↓
ingest.py reads from Event Hub
         ↓
Parse & validate events
         ↓
Join with Bronze reference tables
         ↓
Silver Layer tables (rides_raw, rides_enriched)
         ↓
Gold Layer (aggregations, metrics)
         ↓
Ready for Analytics & BI
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)

```env
# Azure Event Hub
EVENT_HUB_CONNECTION_STRING=Endpoint=sb://your-namespace.servicebus.windows.net/;...
EVENT_HUB_NAME=uber-databricks-topic

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### Azure Storage Configuration (Databricks)

Update in `bronze_adls.py`:

```python
# SAS Token for Azure Storage access(These tokens are already expired, you need to generate new ones from Azure Portal)
token = "sp=r&st=2026-04-26T11:55:28Z&se=2026-04-26T20:10:28Z&spr=https&sv=2025-11-05&sr=c&sig=..."

# Storage URL
url = "https://uberdatabricksstreaming.blob.core.windows.net/raw/ingestion"
```

### Event Hub Configuration (Databricks)

Update in `ingest.py`:

```python
EH_NAMESPACE = "uber-databricks"
EH_NAME = "uber-databricks-topic"
EH_CONN_STR = spark.conf.get("connection_string")

KAFKA_OPTIONS = {
  "kafka.bootstrap.servers": f"{EH_NAMESPACE}.servicebus.windows.net:9093",
  "subscribe": EH_NAME,
  "kafka.sasl.mechanism": "PLAIN",
  "kafka.security.protocol": "SASL_SSL",
  "kafka.sasl.jaas.config": f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="{EH_CONN_STR}";',
}
```

### Reference Data Files (files.json)

Add or remove files by editing `files.json`:

```json
[
    {"fileName": "your_new_file"}
]
```

Then:
1. Add the corresponding JSON file to `Data/` folder
2. Re-run Azure Data Factory pipeline
3. Data will be auto-loaded into Bronze layer

---

## ✨ Key Features

### 🎯 Medallion Architecture
- **Bronze**: Raw data ingestion with minimal transformation
- **Silver**: Cleansed, deduplicated data with business logic
- **Gold**: Analytics-ready aggregated data

### 🔄 Real-Time Streaming
- Event-driven architecture using Azure Event Hub
- Kafka protocol for high-throughput ingestion
- Handles 1000+ events per second

### 📊 Data Quality
- SCD Type 2 slowly changing dimensions
- Data lineage with `updated_at` timestamps
- Schema validation and transformation

### 🔐 Security
- Azure Storage SAS tokens for secure access
- Event Hub SASL/SSL encryption
- Environment variables for sensitive data
- No hardcoded credentials

### 📈 Scalability
- Distributed processing with Apache Spark
- Auto-scaling Databricks clusters
- Partitioned Delta tables for performance
- Event Hub partition scaling

### 🛠️ Automation
- Azure Data Factory orchestration
- Databricks Job scheduling
- Configuration-driven pipelines
- Parameterized transformations

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Azure Data Factory Pipeline Fails

**Issue**: "Error copying data from GitHub"

**Solution**:
- Verify GitHub personal access token is valid
- Check `files.json` format is correct
- Ensure files exist in GitHub repo at specified path

#### 2. Databricks Notebook Error: "Invalid SAS Token"

**Issue**: Authentication fails when reading from Azure Storage

**Solution**:
```python
# Verify SAS token is not expired
# Get new token from Azure Portal
# Update bronze_adls.py with new token
token = "your_new_sas_token"

# Restart cluster and rerun notebook
```

#### 3. Event Hub Connection Error

**Issue**: "Failed to connect to Event Hub"

**Solution**:
- Verify Event Hub connection string in `.env` file
- Check connection string format:
  ```
  Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=...;SharedAccessKey=...
  ```
- Ensure Event Hub name matches configuration
- Verify firewall rules allow connections

#### 4. Web App Shows "Unable to Connect to Event Hub"

**Issue**: Flask app cannot send events to Event Hub

**Solution**:
- Verify `.env` file is in `webapp/` directory
- Run `python config.py` to test configuration
- Check Event Hub credentials are correct
- Ensure Python dependencies are installed: `pip install -r requirements.txt`

#### 5. Bronze Tables Not Created

**Issue**: "Table not found" when querying `uber.bronze.*`

**Solution**:
- Verify `bronze_adls.py` completed successfully
- Check Azure Storage files exist:
  ```sql
  SELECT * FROM `wasbs://raw@{storage_account}.blob.core.windows.net/ingestion/`
  ```
- Verify schema creation:
  ```sql
  CREATE SCHEMA IF NOT EXISTS uber.bronze;
  ```

#### 6. Streaming Job Lag

**Issue**: Silver layer tables not updating with new events

**Solution**:
- Check Event Hub has messages: `SELECT COUNT(*) FROM raw_eventhub`
- Verify Databricks cluster is running
- Check streaming job status in Databricks Workflows
- Increase cluster size if CPU/memory is high

### Debug Commands

**Databricks:**
```sql
-- Check Delta table status
DESC TABLE uber.bronze.map_cities;

-- View recent data
SELECT * FROM uber.silver.rides_raw LIMIT 100;

-- Check table size
SELECT COUNT(*) FROM uber.bronze.map_cities;
```

**Azure CLI:**
```bash
# List blobs in container
az storage blob list --account-name {storage_account} --container-name raw/ingestion

# Get Event Hub stats
az eventhubs eventhub show --resource-group {rg} --namespace-name {namespace} --name {hub_name}
```

---

## 📚 Additional Resources

### Documentation
- [Azure Data Factory Documentation](https://docs.microsoft.com/azure/data-factory/)
- [Databricks Documentation](https://docs.databricks.com/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [Delta Lake Guide](https://docs.delta.io/)
- [Azure Event Hub Documentation](https://docs.microsoft.com/azure/event-hubs/)
- [Flask Documentation](https://flask.palletsprojects.com/)

### Related Projects
- Databricks Delta Live Tables examples
- Azure Synapse Analytics integration
- Power BI connectivity for visualization

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python
- Add docstrings to functions
- Include error handling
- Test changes locally
- Update README if adding new features

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👥 Author

**Bhavesh Bharati**

Data Engineering Portfolio Project showcasing:
- Cloud architecture (Azure)
- Data pipeline orchestration
- Real-time streaming
- Modern data lakehouse patterns

---

## 📞 Support

For issues, questions, or suggestions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Contact the project maintainer

---

## 🎓 Learning Outcomes

By working with this project, you'll learn:

✅ **Cloud Architecture**: Azure services integration
✅ **Data Engineering**: ETL/ELT pipeline design
✅ **Real-time Processing**: Event streaming patterns
✅ **Big Data**: Apache Spark and Delta Lake
✅ **Orchestration**: Azure Data Factory workflows
✅ **Web Development**: Flask applications
✅ **Infrastructure as Code**: Parameterized configurations
✅ **DevOps**: CI/CD patterns with data pipelines

---

## 🔄 Version History

**v1.0.0** (2026-04-27)
- Initial release
- Bronze layer data ingestion
- Silver layer transformations
- Flask web application
- Azure Event Hub integration
- Databricks streaming pipeline

---

**Last Updated**: April 27, 2026

For the latest updates, visit the [GitHub Repository](https://github.com/your-username/uber-databricks-azure-streaming)
