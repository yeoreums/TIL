# TIL: Mann–Whitney U Test for validating ML signals

## What it is

A statistical test that checks whether one group genuinely has **larger values** than another — **without assuming a normal distribution**.

Instead of comparing averages, it:

1. Combines values from both groups
2. Ranks them together
3. Checks whether one group consistently appears higher in the rankings

If yes → the difference is likely real, not random.

---

## When to use it (instead of t-test)

Use Mann–Whitney when:

* Data is skewed or heavy-tailed
* There are outliers
* Distribution shape is unknown
* Working with financial / market data (usually non-normal)

---

## ELI12

Two classes take the same exam.

Instead of comparing average scores, you:

* Put **all students together**
* Rank them from lowest to highest
* Check if students from one class appear **more often near the top**

If they do → that class really performed better.

**p-value**

* p < 0.05 → real difference
* p ≥ 0.05 → could be luck

---

## My use case (Binance Anomaly Project)

Question:
Do anomaly windows actually precede larger future price movement?

Result (5-minute lookahead):

```
if_only vs normal : p=0.000000 ✓ SIGNIFICANT
both vs normal    : p=0.000000 ✓ SIGNIFICANT
```

This confirms:

* IF-only anomalies → ~1.37× larger future moves
* Both (IF + volatility) → ~1.92× larger moves

The effect is **statistically significant**, not random.

---

## Key lesson

A higher average means nothing without statistical validation.

**Always test significance before trusting a signal.**
 