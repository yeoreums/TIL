# TIL – Batch Candle → Silver DAG (Airflow + Snowflake)

## What I built

I implemented a batch Airflow DAG that loads Upbit candle data from S3 into Snowflake Silver layer.
- Source: Parquet files in S3 (daily partition)
- Target: UPBIT_DB.SILVER.SILVER_CANDLES
- Candle intervals: 1m / 5m / 1h / 1d
- One unified Silver table for all intervals

---
### Data flow
```
S3 (Parquet)
  → Pandas DataFrame
    → Schema normalization (Raw → Silver)
      → Timezone-aware date derivation (UTC → KST)
        → Snowflake (write_pandas)
```

S3 path convention:
```
yymmdd=YYYY-MM-DD/
  ├─ candle_1min.parquet
  ├─ candle_5min.parquet
  ├─ candle_1hour.parquet
  └─ candle_days.parquet
```
---
## Key implementation details
### 1. Interval derivation from filename

Raw data does not include candle interval as a column, so it is derived from the filename at the Silver layer.
```
candle_1min   → 1m
candle_5min   → 5m
candle_1hour  → 1h
candle_days   → 1d
```
This keeps the Raw layer untouched.

---
### 2. Explicit timestamp handling (critical)

Upbit candle timestamps are epoch milliseconds.
```python
CANDLE_TS = pd.to_datetime(
    CANDLE_TS,
    unit="ms",
    utc=True
)
```

Without explicit conversion, timestamps were silently interpreted as `1970-01-01`, which caused incorrect `TRADE_DATE` values.

---

### 3. TRADE_DATE definition (UTC vs KST)

TRADE_DATE is derived in KST (Asia/Seoul) for analytics and partitioning.
```python
TRADE_DATE = (
    CANDLE_TS
      .dt.tz_convert("Asia/Seoul")
      .dt.date
)
```

Important clarification:
- Running the DAG on `2025-12-17`
- Loading 2025-12-16 candle data

    → This behavior is expected and correct

---
### 4. Fail-fast schema validation

Before loading into Snowflake:
- Validate required columns
- Abort immediately if schema mismatch occurs

This prevented silent data corruption.

---
### 5. Snowflake loading strategy

- Used `write_pandas`
- Append-only strategy (for now)
- Uppercase column names to match Snowflake conventions

Future improvement:
- Date-based overwrite (`MERGE INTO`) for idempotency

---
## Debugging lessons learned
### Problem 1: `1970-01-01` in TRADE_DATE

Cause:
- Timestamp was not explicitly converted from epoch ms

Fix:
- Always specify unit="ms" when parsing Upbit timestamps

---
### Problem 2: COUNT kept increasing unexpectedly

Cause:
- Append-only loading + repeated test runs

Resolution:
- Expected behavior
- Highlighted the need for idempotent load logic later

## What I learned
- Time handling must be explicit in data pipelines (timezone + unit)
- Never trust implicit datetime parsing
- Debug logs right before warehouse writes are extremely valuable
- File-based metadata (like interval) can be safely derived in Silver, not Raw
- Append-only pipelines are easy to build but must be documented clearly