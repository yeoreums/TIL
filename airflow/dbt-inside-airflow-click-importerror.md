# Troubleshooting: Running dbt inside Airflow (Click ImportError)
## Context
As part of an Upbit Batch → Gold data pipeline, I needed to run dbt (Snowflake adapter) inside an Airflow environment running on Docker (EC2).

The goal was to manage Gold tables via dbt and later schedule them using Airflow.

During setup, I encountered a blocking runtime error when executing dbt inside the Airflow worker container.

---
## Problem Summary
When running dbt inside the Airflow worker container:
```bash
dbt --version
dbt run
```
The following error occurred:
```bash
ImportError: cannot import name '_OptionParser' from 'click.parser'
```
This happened even though the following packages:
- `dbt-core`
- `dbt-snowflake`

were successfully installed.

---
## Root Cause Analysis
### 1. Dependency conflict: `click`
- Airflow internally depends on the Python package `click`
- dbt also depends on `click`
- dbt imports internal symbols (`_OptionParser`) that were removed in newer versions of click
- The official Airflow image (`apache/airflow:2.9.3`) ships with a newer click version

Result: dbt crashes at runtime due to an incompatible `click` version.

### 2. Why pinning versions did NOT work
I attempted:
- Pinning `dbt-snowflake` to older versions
- Downgrading `dbt-core`
- Switching Python versions (3.12 → 3.10)
All attempts failed because:
- Airflow tightly controls its dependency graph
- Downgrading `click` would break Airflow itself
- Modifying shared dependencies is unsafe in a multi-DAG environment

Conclusion: This is a structural dependency conflict, not a simple version mismatch.

---
## Design Decision: Why I chose a venv
I evaluated two architectural approaches.

### Option A — Isolated Python venv inside Airflow container (chosen)
What it is
- Create a separate Python virtual environment inside the Airflow worker container
- Install `dbt-core` and `dbt-snowflake` only inside that venv
- Airflow and dbt no longer share Python dependencies
Pros
- No impact on existing Airflow DAGs
- Completely avoids `click` conflicts
- Minimal CPU / memory overhead
- Simple and stable
- Common production pattern for Airflow + dbt on EC2
Cons
- dbt is not on PATH by default (must call full path)
Chosen because it is the safest and fastest solution for this project scale

### Option B — Separate dbt container (not chosen)
What it is
- Build a dedicated dbt Docker image
- Run dbt using Airflow `DockerOperator`
Why I didn’t choose it (for now)
- Requires Docker socket mounting
- More infrastructure complexity
- Higher runtime overhead
- Overkill for a small-to-medium project
Kept as a future option if dbt workloads grow significantly.

---
## Final Implementation
### 1. Extend Airflow image with dbt venv
Created a custom `Dockerfile`:
```
FROM apache/airflow:2.9.3

USER root

RUN python3 -m venv /opt/dbt_venv && \
    /opt/dbt_venv/bin/pip install --no-cache-dir dbt-core dbt-snowflake

RUN chown -R airflow:airflow /opt/dbt_venv

USER airflow
```

This isolates dbt completely from Airflow’s Python environment.

### 2. Update `docker-compose.yaml`
Replaced image pull with build:
```yaml
# image: apache/airflow:2.9.3
build: .
```
This ensures:
- Airflow worker uses the extended image
- Existing DAGs remain unaffected

### 3. Verify dbt inside the Airflow worker
Inside the worker container:
```bash
/opt/dbt_venv/bin/dbt --version
```
Result:
```
dbt-core 1.10.17
dbt-snowflake 1.10.6
```
dbt runs successfully without click errors.

## dbt Project Setup
- dbt project location:
```
batch/dbt/
```
- Project name:
```
upbit_dbt
```
- Gold models:
```
batch/dbt/models/gold/
```
- Snowflake schema mapping handled via dbt_project.yml

## Validation
- Ran:
```bash
dbt run --select gold
```
- Confirmed table creation:
```
UPBIT_DB.GOLD.GOLD_CANDLE_WINDOW_METRICS
```
- Verified `LAST_ALTERED` timestamp matched dbt execution time
(timezone difference explained: Snowflake session timezone ≠ KST)

## Troubleshooting Checklist (If this happens again)
Symptom
```
ImportError: cannot import name '_OptionParser' from 'click.parser'
```
Do NOT
- Downgrade click globally
- Install dbt into Airflow’s base Python environment
Do
- Use an isolated venv (/opt/dbt_venv)
- Run dbt via full path
- Build a custom Airflow image
- Verify worker container uses the built image

### Key Takeaway

> dbt should never share Python dependencies with Airflow in Docker unless carefully isolated.

Using a dedicated venv inside the Airflow worker provides:
- Stability
- Reproducibility
- Zero impact on other DAGs
For this project stage, this is the right engineering trade-off.
