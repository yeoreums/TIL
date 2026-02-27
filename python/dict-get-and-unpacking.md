# Python TIL: Aggregation with `dict.get()` and unpacking

## Problem

When processing structured rows, we often need to sum values by a key.

Example row:

```python
(date, product, category, amount)
```

Goal:

```
category → total amount
```

---

## Using tuple unpacking

Instead of indexing:

```python
for row in rows:
    category = row[2]
    amount = row[3]
```

Use unpacking:

```python
for date, product, category, amount in rows:
    ...
```

If some fields are not needed:

```python
for _, _, category, amount in rows:
    ...
```

`_` is used for values that are intentionally ignored.

---

## Using `dict.get()` for aggregation

Instead of manual initialization:

```python
if category not in totals:
    totals[category] = 0

totals[category] += amount
```

Use:

```python
totals[category] = totals.get(category, 0) + amount
```

Meaning:

* If key exists → use current value
* If not → start from 0
* Then add the new amount

---

## Why this pattern matters

This combination is common in:

* Data processing scripts
* Log analysis
* Backend metrics
* ETL pipelines

It is the manual version of:

* SQL `GROUP BY`
* Pandas `groupby().sum()`

---

## Summary

| Pattern            | Use                                     |
| ------------------ | --------------------------------------- |
| Tuple unpacking    | Access structured fields safely         |
| `_`                | Ignore unused values                    |
| `dict.get(key, 0)` | Aggregate without manual initialization |
