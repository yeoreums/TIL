# Python TIL: enumerate()

## What is `enumerate()`

`enumerate()` allows you to loop over an iterable while keeping track of the index.

Instead of manually managing indices with `range(len())`, `enumerate()` provides a cleaner and more Pythonic approach.

---

## Basic Usage

Without `enumerate()`

```python
items = ["apple", "banana", "orange"]

for i in range(len(items)):
    print(i, items[i])
```

With `enumerate()`

```python
items = ["apple", "banana", "orange"]

for i, item in enumerate(items):
    print(i, item)
```

Output

```
0 apple
1 banana
2 orange
```

---

## Start Index Option

You can change the starting index using the `start` parameter.

```python
items = ["apple", "banana", "orange"]

for i, item in enumerate(items, start=1):
    print(i, item)
```

Output

```
1 apple
2 banana
3 orange
```

---

## Practical Example (CLI-style)

Useful when displaying numbered options to users.

```python
purchases = [("food", 10), ("coffee", 5)]

for i, (category, amount) in enumerate(purchases, start=1):
    print(i, category, amount)
```

---

## Why use `enumerate()`

Better than:

```python
for i in range(len(items)):
```

Because it:

* Improves readability
* Reduces indexing mistakes
* Follows Python best practices (Pythonic code)

---

## When to use

Use `enumerate()` when:

* You need both index and value
* Printing numbered lists
* Processing ordered data
* Building CLI menus or logs

---

## Summary

| Pattern                        | Use                       |
| ------------------------------ | ------------------------- |
| `enumerate(iterable)`          | Get index + value         |
| `enumerate(iterable, start=1)` | Custom starting index     |
| Avoid `range(len())`           | Prefer Pythonic iteration |

---

## Related

Often used with:

* List processing
* File reading loops
* Data pipelines (row indexing)
* CLI applications
