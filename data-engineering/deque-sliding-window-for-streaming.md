# deque(maxlen) behavior in Python

## Context

While reviewing feedback on my anomaly detection logic, I learned that `collections.deque` automatically removes the oldest element when `maxlen` is reached.

This means explicit deletion logic is not required.

## Example

```python
from collections import deque

window = deque(maxlen=3)

window.append(1)
window.append(2)
window.append(3)
print(window)  # deque([1, 2, 3], maxlen=3)

window.append(4)
print(window)  # deque([2, 3, 4], maxlen=3)
```

## Why this works

- `deque` maintains FIFO order.
- When `maxlen` is exceeded, the leftmost (oldest) element is removed automatically.
- `append` remains O(1).

## Why this is useful in streaming

In real-time streaming systems:

- Data arrives continuously.
- Only the most recent N values matter.
- Old data must be discarded efficiently.

Using `deque(maxlen=N)` provides:

- A fixed-size sliding window.
- Automatic eviction.
- Clear and concise code.

## Applied in my project

- Project: Upbit real-time data pipeline
- Use case: Price / volume anomaly detection
- Approach: Sliding window over recent ticks using `deque(maxlen)`

This let me focus on detection logic rather than window management.
