# TIL – Batch Trade → Silver DAG (Airflow + Snowflake)
## What I built

I implemented a batch Airflow DAG that loads Upbit trade (tick) data from S3 into the Snowflake Silver layer.
- Source: Trade parquet files in S3 (daily partition)
- Target: UPBIT_DB.SILVER.SILVER_TRADES
- Data type: Trade-level (tick) data
- Strategy: Append-only Silver ingestion

---
## Data flow
```
S3 (Trade Parquet)
  → Pandas DataFrame
    → Schema normalization (Raw → Silver)
      → Timestamp parsing (epoch ms → UTC)
        → KST-based TRADE_DATE derivation
          → Snowflake (write_pandas)
```

S3 path convention:
```
yymmdd=YYYY-MM-DD/
  └─ trade.parquet
```
---
## Key implementation details
1. Defensive handling of upstream schema changes

The Raw Trade data did not consistently expose the same timestamp column name.

Observed upstream schema:
```
timestamp
trade_date_utc
trade_time_utc
```

Instead of enforcing a strict assumption, the Silver DAG detects the timestamp column dynamically.
```python
if "trade_timestamp" in df.columns:
    ts_col = "trade_timestamp"
elif "timestamp" in df.columns:
    ts_col = "timestamp"
else:
    raise ValueError("No timestamp column found in raw trade data")
```

This approach:
- Keeps the Raw layer unchanged
- Makes the Silver DAG resilient to upstream schema variations
- Prevents unnecessary Raw DAG refactors

---
## 2. Explicit timestamp parsing (epoch milliseconds)

Upbit trade timestamps are provided as epoch milliseconds (UTC).
```python
TRADE_TS = pd.to_datetime(
    TRADE_TS,
    unit="ms",
    utc=True
)
```

Explicit conversion is mandatory.
Without specifying `unit="ms"`, timestamps can be silently misinterpreted.

---
## 3. TRADE_DATE derivation (UTC → KST)

For analytics and downstream aggregation, `TRADE_DATE` is derived in Korean Standard Time (Asia/Seoul).
```python
TRADE_DATE = (
    TRADE_TS
      .dt.tz_convert("Asia/Seoul")
      .dt.date
)
```

Example:

`TRADE_TS`: `2025-12-17 23:59:58 UTC`

`TRADE_DATE`: `2025-12-18 (KST)`

This behavior is intentional and correct.

---
## 4. Optional column normalization

Some trade attributes may not always exist upstream:
- `PREV_CLOSING_PRICE`
- `CHANGE_PRICE`
- `ASK_BID`
- `SEQUENTIAL_ID`

To keep Snowflake inserts stable, missing optional columns are explicitly created as `NULL`.
```python
for col in optional_cols:
    if col not in df.columns:
        df[col] = None
```

This avoids schema-related insert failures.

---
## 5. Fail-fast schema validation

Before loading into Snowflake:
- Required columns are validated
- DAG fails immediately on schema mismatch

This prevents partial or silently corrupted Silver data.

---
## 6. Snowflake loading strategy

- Used write_pandas
- Append-only ingestion
- `SOURCE = 'batch_trade'` added for lineage tracking

Future improvement:
- Idempotent loads using date-based `MERGE INTO`

---
## Testing & validation

- Environment: Airflow sandbox (Docker)
- Test method:

```bash
airflow tasks test batch_trade_to_silver_dag load_trades_to_snowflake 2025-12-18
```

Result:
- 40,000 trade rows loaded
- Successful Snowflake insert
```
Snowflake write complete: success=True, rows=40000
```

---
## Debugging lessons learned
### Problem 1: Missing `trade_timestamp` column

Cause:
- Silver DAG assumed a fixed column name
- Actual Raw schema used timestamp

Fix:
- Defensive timestamp column detection

---
### Problem 2: Append-only test runs increasing row counts

Cause:
- Multiple manual test executions

Resolution:
- Expected behavior
- Reinforced the need to clearly document append-only pipelines

---
## What I learned
- Raw data contracts should be respected; consumers must adapt
- Defensive schema handling greatly improves pipeline stability
- Timestamp parsing must always be explicit (unit + timezone)
- Silver layer is the correct place for normalization, not Raw
- Sandbox Airflow testing prevents costly production failures