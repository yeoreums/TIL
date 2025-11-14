# [TIL] Making Slack Notification DAG Visible in Airflow UI with `.airflowignore`

### 🗓️ Date
2025-11-13

---

## 🧩 Issue

While setting up **Slack alerts** in my Airflow project (running on Docker inside Ubuntu WSL),  
I created a test DAG called `test_slack_alert_on_failure.py` to send a message to Slack when triggered.  

Even though the file was correctly located in:
/opt/airflow/dags/

the DAG **did not appear in the Airflow Web UI** (`http://localhost:8080`).

I confirmed that the file existed inside the scheduler container:
```bash
docker exec -it learn-airflow-airflow-scheduler-1 ls /opt/airflow/dags
```

But still, nothing showed up on the UI. No parsing errors, no DAG import failure — it was just invisible.

<img width="3795" height="1983" alt="Screenshot 2025-11-11 154640" src="https://github.com/user-attachments/assets/78a9726e-320c-465d-8fc5-193c4b8ec824" />

---
## 🔍 Root Cause

By checking import logs:
```bash
airflow dags list-import-errors
```
I discovered multiple DAGs were failing during parsing with errors like:

KeyError: 'Variable csv_url'

KeyError: 'Variable open_weather_api_key'

ModuleNotFoundError: No module named 'oauth2client'

ModuleNotFoundError: No module named 'yfinance'

Since Airflow loads all DAGs on import, these exceptions prevented my new DAG from being parsed and displayed.
---
## 🧠 Solution

To isolate my test DAG and safely test Slack notifications, I followed these steps:

### 1️⃣ Add Defensive Code in ```plugins/slack.py```

Prevent import failure by wrapping the Slack webhook variable in a try/except block:
```python
from airflow.models import Variable
import requests

def on_failure_callback(context):
    try:
        slack_url = Variable.get("slack_url")
    except KeyError:
        # Fallback webhook for testing (replace with your own)
        slack_url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"

    text = str(context['task_instance']) + "```" + str(context.get('exception')) + "```"
    headers = {'content-type': 'application/json'}
    data = {"username": "Data GOD", "text": text, "icon_emoji": ":scream:"}
    requests.post(slack_url, json=data, headers=headers)
```

This way, even if the slack_url Variable wasn’t defined in Airflow,
the plugin would not crash during import.

### 2️⃣ Create a Minimal Test DAG

```dags/test_slack_alert_on_failure.py```:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from plugins import slack

def intentionally_fail():
    raise ValueError("Slack alert test: intentional failure")

with DAG(
    dag_id='test_slack_alert_on_failure',
    start_date=datetime(2025, 11, 12),
    schedule_interval=None,
    catchup=False,
    on_failure_callback=slack.on_failure_callback,
) as dag:
    fail = PythonOperator(task_id='trigger_failure', python_callable=intentionally_fail)
```

### 3️⃣ Ignore Problematic DAGs Temporarily

Some existing DAGs (using Redshift, Google Sheets, and APIs) caused import errors because dependencies weren’t configured.
To prevent these from breaking the scheduler, I updated .airflowignore in the dags/ folder:

# Ignore failing Redshift-related DAGs temporarily
^NameGenderCSVtoRedshift.*\.py$
^Weather_to_Redshift.*\.py$
^Gsheet_to_Redshift.*\.py$
^SQL_to_Sheet.*\.py$
^UpdateSymbol.*\.py$


This allowed Airflow to skip those files and successfully parse the rest, including my Slack test DAG.

### 4️⃣ Adjust Docker Environment

Updated docker-compose.yaml to ensure correct data and environment variables:
```yaml
environment:
  AIRFLOW_VAR_SLACK_URL: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"
  _PIP_ADDITIONAL_REQUIREMENTS: "${_PIP_ADDITIONAL_REQUIREMENTS:-requests oauth2client yfinance}"
volumes:
  - ./data:/opt/airflow/data
```

### 5️⃣ Restart Airflow
```bash
docker-compose down
docker-compose rm -f
docker-compose up -d
```
After the restart:

✅ The import errors disappeared

✅ The test_slack_alert_on_failure DAG appeared on the UI

✅ Slack notification test succeeded 🎉

---

## 💡 What I Learned

* Import-time exceptions (Variable or missing dependency) can prevent all DAGs from loading.

* ```.airflowignore``` is powerful for isolating or temporarily disabling problematic DAGs.

* Use try/except defensively in plugins to make imports resilient.

* Always check import errors with ```airflow dags list-import-errors```.

* Keep ```_PIP_ADDITIONAL_REQUIREMENTS``` updated for missing packages like requests, oauth2client, and yfinance.
---
✅ Key Commands Recap
```bash
# Check all DAG import errors
airflow dags list-import-errors

# Restart Airflow
docker-compose down
docker-compose up -d

# Inspect DAG files inside container
docker exec -it learn-airflow-airflow-scheduler-1 ls /opt/airflow/dags
```

## 🚀 Result

After cleaning up ```.airflowignore``` and resolving import issues,
```test_slack_alert_on_failure.py``` appeared properly in the Airflow Web UI,
and Slack notifications worked exactly as expected.

<img width="3571" height="1692" alt="Screenshot 2025-11-12 211837" src="https://github.com/user-attachments/assets/3d828c76-950a-4910-8671-e048758bb7b5" />

---
Checking running dags on Airflow Web UI:

<img width="1520" height="473" alt="Screenshot 2025-11-13 132637" src="https://github.com/user-attachments/assets/74583378-a6fa-4290-8966-bcc55479b4f8" />
