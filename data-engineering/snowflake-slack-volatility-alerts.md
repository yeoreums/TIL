# 🚀 Building a Stock Volatility Alert System with Snowflake & Slack

## Project Context

As part of my Data Engineering Bootcamp team project, I built an end-to-end pipeline to detect market volatility. The goal was to monitor NASDAQ and S&P 500 stocks and trigger a **Slack notification** only when a stock's hourly movement was statistically significant.

**Tech Stack:** Snowflake, Airflow, Slack Webhooks, SQL (Stored Procedures)

---

## 1. Architecture Flow

1. **Ingestion:** Stock data is loaded from S3 into Snowflake (`ECONOMIC_DATA.RAW_DATA.STOCK_PRICES`)
2. **Processing:** A Snowflake Stored Procedure calculates intra-day volatility using window functions
3. **Alerting:** If `Abs(Log Return) > 2.0 * Hourly_Stdev`, a notification is sent to Slack via Webhook

---

## 2. Snowflake Setup

I secured the Slack Webhook URL using Snowflake's `SECRET` and `NOTIFICATION INTEGRATION` objects to avoid hardcoding credentials.

```sql
-- Integration Setup
CREATE OR REPLACE NOTIFICATION INTEGRATION slack_webhook_int
    TYPE = WEBHOOK
    ENABLED = TRUE
    WEBHOOK_URL = 'https://hooks.slack.com/services/SNOWFLAKE_WEBHOOK_SECRET'
    WEBHOOK_SECRET = slack_webhook_secret 
    WEBHOOK_HEADERS = ('Content-Type' = 'application/json')
    WEBHOOK_BODY_TEMPLATE = '{"text": "SNOWFLAKE_WEBHOOK_MESSAGE"}'
    COMMENT = 'Slack Integration';
```

---

## 3. The Logic: Dynamic Volatility

Instead of a fixed percentage (e.g., "Alert on every 1% move"), I implemented a dynamic threshold based on Standard Deviation (2.0σ). This normalizes volatility across different assets (e.g., TSLA vs. AAPL).

**The Logic:**
- Calculate Hourly Log Returns using `LN(CLOSE / LAG(CLOSE) ...)`
- Calculate Hourly Standard Deviation for the specific ticker
- **Trigger Condition:** Alert if the move is `> 2.0 × Hourly_Stdev`

---

## 4. Verification & Tuning Results

This was the most critical step. I needed to ensure the alert was sensitive enough to catch crashes but not so sensitive that it spammed the channel.

### Phase 1: Stress Test (Low Threshold)

I initially tested the pipeline with a very low threshold (`0.001 * Stdev`) to verify the Slack connection.

- **Result:** The pipeline successfully fired 51 notifications for 77 data points
- **Analysis:** The pipeline works, but it is too noisy for production

### Phase 2: Production Tuning (2.0 Sigma)

I adjusted the threshold to the industry standard for "rare events" (`2.0 * Stdev`).

- **Result:** The system filtered out the noise and triggered exactly 1 notification
- **The Catch:** It correctly identified a 1.86% hourly move in TSLA as a volatility event, while ignoring smaller moves in stable stocks like AAPL
<img width="738" height="559" alt="image" src="https://github.com/user-attachments/assets/b5b7d6ca-2fe5-4a09-a953-78489c91f522" />

---

## 5. Troubleshooting: The Loop Error

During development, I encountered a persistent error when using a standard `FOR` loop in Snowflake:

```
Error: invalid identifier 'ALERT_ROW.TICKER'
```

### The Problem

When looping over a `SELECT *` result in a Stored Procedure, Snowflake struggled to identify column names inside the loop variable (`alert_row`), causing identifier errors despite various aliasing attempts.

### The Solution

I refactored the code to use an **Explicit Cursor with a WHILE loop**.

1. Declare local variables (`v_TICKER`, `v_CHANGE_PERCENT`, etc.)
2. Use `FETCH c_alerts INTO ...` to map columns directly to variables
3. This removed the ambiguity and allowed the procedure to compile and run perfectly

---

## 6. Automation (Airflow)

Finally, I integrated this into the Airflow DAG using the `SnowflakeOperator`.

```python
snowflake_alert_task = SnowflakeOperator(
    task_id='run_volatility_alerts',
    sql="CALL ECONOMIC_DATA.RAW_DATA.SP_SEND_VOLATILITY_ALERT();",
    snowflake_conn_id='snowflake_conn',
    dag=dag,
)
```

---

## Final Result

A robust alert system that runs automatically after data ingestion, providing the team with real-time insights into significant market anomalies without false positives.

---

**Tags:** `#snowflake` `#slack` `#data-engineering` `#airflow` `#sql` `#stored-procedures` `#webhooks` `#alerts`
