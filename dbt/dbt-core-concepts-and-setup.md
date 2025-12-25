# 🧱 dbt (Data Build Tool): Core Concepts & Setup Guide

This document summarizes the essential concepts, setup steps, and commands for integrating dbt into a data engineering pipeline (Airflow + Snowflake). It serves as a quick reference for the T (Transform) layer in ELT.

## 🚀 The Big Picture: ELT Workflow

In a modern data stack, dbt handles the transformation logic after data is loaded into the warehouse.

1. **Extract & Load (Airflow)**: S3 files → Snowflake (RAW_DATA schema)
2. **Transform (dbt)**: Cleans, joins, and aggregates data → Snowflake (ANALYTICS schema)
3. **Analyze (BI Tools)**: Final tables are consumed by dashboards

## 🔑 Key Concepts

### 1. Models (.sql)

A model is a single `.sql` file containing a SELECT statement. dbt executes this SQL to create tables or views in the warehouse.

- **Dependency Management**: Use `{{ ref('model_name') }}` to reference other models. dbt builds the execution order (DAG) automatically.
- **Source Referencing**: Use `{{ source('source_name', 'table_name') }}` to reference raw data tables.

### 2. Materializations

Defines how dbt builds models in the warehouse. Configured in `dbt_project.yml` or the SQL file itself.

| Type | Description | Best Use Case |
|------|-------------|---------------|
| **View** | `CREATE VIEW` | Staging layers, lightweight transformations |
| **Table** | `CREATE TABLE AS` | Final analytics tables (Marts), high-performance query needs |
| **Incremental** | Updates changed rows only | Large fact tables (event logs, transaction history) |
| **Ephemeral** | CTE (Common Table Expression) | Intermediate logic reused across multiple models but not stored |

### 3. Profiles (profiles.yml)

Holds database connection credentials (e.g., Snowflake account, user, password).

- **Location**: `~/.dbt/profiles.yml` (Local) or mounted volume (Docker)
- **Security**: Never commit this file to Git!

## 🛠️ Step-by-Step Implementation

### 1. Project Structure

A standard dbt project organizes models into layers:

- `models/staging/`: 1:1 mapping with raw data. Renaming columns, casting types. (Materialized as View)
- `models/marts/`: Business logic, joins, aggregations. (Materialized as Table)

### 2. Defining Sources (sources.yml)

Tell dbt where the raw data lives.

```yaml
version: 2

sources:
  - name: raw_stock_data
    database: ECONOMIC_DATA
    schema: RAW_DATA
    tables:
      - name: stock_prices
```

### 3. Writing a Staging Model (stg_stocks.sql)

Clean up the raw data using Jinja macros.

```sql
SELECT
    -- Generate a unique ID
    {{ dbt_utils.generate_surrogate_key(['ticker', 'datetime']) }} as id,
    ticker as symbol,
    open as open_price,
    volume,
    created_at
FROM {{ source('raw_stock_data', 'stock_prices') }}
```

## 📘 Essential dbt Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `dbt debug` | Test connection to the warehouse | `dbt debug` |
| `dbt run` | Run all models | `dbt run` |
| `dbt run --select <model>` | Run a specific model only | `dbt run -s stg_stocks` |
| `dbt run --select +<model>` | Run a model and all its parents | `dbt run -s +fct_daily_sales` |
| `dbt test` | Execute tests defined in .yml files | `dbt test` |
| `dbt compile` | Compile Jinja SQL to raw SQL (check target/) | `dbt compile` |
| `dbt docs generate` | Generate documentation site | `dbt docs generate` |

## 🐳 Airflow Integration (Docker + WSL Tips)

Integrating dbt into Airflow running on Docker/WSL requires careful configuration to avoid performance bottlenecks and path errors.

### 1. Dockerfile Setup

Ensure the Airflow image includes the dbt adapter.

**File**: `requirements.txt`  
**Content**: `dbt-snowflake==1.7.0` (Pin version to avoid dependency conflicts)

### 2. Volume Mounting (docker-compose.yml)

You must mount the project files into the container so Airflow can access them.

```yaml
volumes:
  - ./dags:/opt/airflow/dags
  - ./dbt_analytics:/opt/airflow/dbt_analytics  # Mount dbt project
  - ./profiles.yml:/home/airflow/.dbt/profiles.yml:ro # Mount profile config
```

### 3. WSL Performance Tuning (Critical)

When running Docker on Windows (WSL2), **never keep your project files on the Windows filesystem** (`/mnt/c/...`).

- **Problem**: File I/O is extremely slow across the Windows-Linux boundary, causing the Airflow Scheduler to hang or crash.
- **Solution**: Move the entire project to the WSL native filesystem (e.g., `~/project` or `/home/user/project`).

### 4. Airflow Task (BashOperator)

Use the BashOperator to execute dbt commands inside the container.

```python
run_dbt = BashOperator(
    task_id="run_dbt_transformation",
    # Navigate to the mounted dbt project folder and run
    bash_command="cd /opt/airflow/dbt_analytics && dbt run",
    dag=dag
)
```

---

**Tags**: `#dbt` `#data-engineering` `#ELT` `#airflow` `#snowflake` `#docker` `#wsl`
