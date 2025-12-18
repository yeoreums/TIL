# TIL – Deploying Airflow DAGs on EC2 (Docker)
## Context
Airflow is running on EC2 using Docker containers.
Even though Airflow has a Web UI, DAG code should be managed outside the UI and deployed via the EC2 host.

## Why I didn’t use Airflow Web UI

I learned that writing DAG code directly in the Airflow Web UI is not a good practice because:
- Changes are not tracked in Git
- No code review or rollback
- Errors affect production immediately
- No IDE support (linting, autocomplete, Copilot)
The Web UI should be used only for:
- Triggering DAGs
- Checking logs
- Pausing / unpausing pipelines

## Actual deployment flow I used
```
Local (WSL + VSCode)
  → GitHub PR
    → EC2 (scp + sudo mv)
      → Airflow container test
        → Web UI verification
```

## Commands I used today
### 1. Connect to EC2
```bash
ssh -i ~/.ssh/de7-team6-key.pem ec2-user@<EC2_PUBLIC_IP>
```

### 2. Copy DAG file to EC2 (safe way)
Direct copy to DAG folder may fail due to permissions, so I used `/tmp` first.

```bash
scp -i ~/.ssh/key.pem \
~/upbit-data-pipeline/batch/dags/silver/batch_trade_to_silver_dag.py \
ec2-user@<EC2_PUBLIC_IP>:/tmp/
```

### 3. Move DAG file into Airflow DAG directory
```bash
sudo mv /tmp/batch_trade_to_silver_dag.py /home/ec2-user/airflow/dags/
```

Check:
```bash
ls /home/ec2-user/airflow/dags | grep batch_trade
```

### 4. Enter Airflow scheduler container
```bash
docker exec -it airflow-airflow-scheduler-1 /bin/bash
```

### 5. Verify DAG is detected
```bash
airflow dags list | grep batch_trade
```

### 6. Test task execution manually
```bash
airflow tasks test \
batch_trade_to_silver_dag \
load_trades_to_snowflake \
2025-12-18
```
This runs the task once without scheduler involvement.

## What I learned
- Airflow DAGs should never be edited in the Web UI
- DAG files must exist on the EC2 host, not just inside containers
- `/tmp → sudo mv → dags/` is a reliable deployment pattern
- airflow tasks test is the fastest way to validate logic in production-like environments
- Web UI is for observability, not development
