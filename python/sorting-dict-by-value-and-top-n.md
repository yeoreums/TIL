# Python TIL: Sorting Dictionary by Value and Getting Top-N

## Problem

Given aggregated data in a dictionary:

```python
totals = {
    "Fruit": 9,
    "Dairy": 12,
    "Bakery": 11
}
```

Goal:

* Sort by value (descending)
* Get the top N results

---

## Step 1: Convert to items

```python
totals.items()
```

Returns:

```
("Fruit", 9)
("Dairy", 12)
("Bakery", 11)
```

Each element is a `(key, value)` tuple.

---

## Step 2: Sort by value

```python
sorted_items = sorted(
    totals.items(),
    key=lambda x: x[1],
    reverse=True
)
```

`lambda x: x[1]` means:
Sort using the **value** (second element of the tuple).

Result:

```
("Dairy", 12)
("Bakery", 11)
("Fruit", 9)
```

---

## Step 3: Get Top-N

```python
N = 2
top_items = sorted_items[:N]
```

---

## Final Pattern

```python
for category, amount in sorted(totals.items(), key=lambda x: x[1], reverse=True)[:N]:
    print(category, amount)
```

---

## Why this matters

This pattern is commonly used in:

* Data analysis scripts
* Log processing
* Backend metrics
* Reporting

Equivalent concepts:

| Tool   | Operation                     |
| ------ | ----------------------------- |
| SQL    | `ORDER BY value DESC LIMIT N` |
| Pandas | `sort_values(...).head(N)`    |

---

## Summary

| Step                              | Purpose                         |
| --------------------------------- | ------------------------------- |
| `dict.items()`                    | Convert to `(key, value)` pairs |
| `sorted(..., key=lambda x: x[1])` | Sort by value                   |
| `reverse=True`                    | Descending order                |
| `[:N]`                            | Get Top-N                       |
