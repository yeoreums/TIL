# Python TIL: next()

## What is `next()`

`next()` gets the next item from an iterator.

File objects are iterators, so `next()` reads one line at a time.

---

## Basic Usage

```python
with open("sales.csv") as file:
    first_line = next(file)
    print(first_line)
```

Reads only the first line.

---

## Practical Example (skip CSV header)

```python
with open("sales.csv") as file:
    next(file)  # skip header

    for line in file:
        print(line.strip())
```

After `next(file)`, the loop starts from the second line.

---

## Comparison: `next()` vs `enumerate()`

Using `next()`:

```python
with open("sales.csv") as file:
    next(file)
    for line in file:
        print(line)
```

Using `enumerate()`:

```python
with open("sales.csv") as file:
    for i, line in enumerate(file):
        if i == 0:
            continue
        print(line)
```

| Method        | When to use                |
| ------------- | -------------------------- |
| `next(file)`  | Simple header skip         |
| `enumerate()` | When you need line numbers |

---

## Common mistake

`next()` works only with iterators.

```python
filename = "sales.csv"
next(filename)  # TypeError
```

Also avoid overwriting the file object.

---

## Summary

| Pattern      | Use                         |
| ------------ | --------------------------- |
| `next(file)` | Read one line / skip header |
| File object  | Acts as an iterator         |
| Alternative  | Use `enumerate()` for index |

---

## Related

Often used with:

* File reading
* CSV processing
* Data pipelines
