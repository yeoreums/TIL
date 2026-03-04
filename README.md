# TIL (Today I Learned)

🧠 Latest TIL
→ enumerate basics

📚 Total TIL entries: 22
📅 Last updated: 2026-03-04

---

A collection of things I learn and fix every day while studying data engineering, Python, Linux, Airflow, and web development.

This repo helps me track my progress, organize solutions to debugging issues, and document concepts in my own words.
> Inspired by [@drecali](https://github.com/drecali)'s [TIL repo](https://github.com/drecali/til) and his advice to document even small learnings early on.
---

## 📂 Categories

### Airflow
- [Troubleshooting: Running dbt inside Airflow (Docker) on EC2](airflow/dbt-inside-airflow-click-importerror.md)
- [Making Slack Notification DAG Visible in Airflow UI with .airflowignore](airflow/airflow-import-error-slack-alert.md)
- [Batch Candle Silver to Snowflake](airflow/batch-candle-to-silver-snowflake.md)
- [Batch Trade Silver to Snowflake](airflow/batch-trade-to-silver-snowflake.md)

### Data Engineering
- [deque sliding window for streaming](data-engineering/deque-sliding-window-for-streaming.md)
- [Stock Volatility Alert System with Snowflake & Slack](data-engineering/snowflake-slack-volatility-alerts.md)

### dbt
- [dbt Troubleshooting notes](dbt/dbt-troubleshooting-note.md)
- [dbt Compilation & schema issues and macro](dbt/dbt-compilation-and-schema-issues.md)
- [dbt Core Concepts & Setup Guide](dbt/dbt-core-concepts-and-setup.md)

### DevOps & system
- [Airflow/Docker/WSL Troubleshooting: Core Commands and Fixes](dev-ops-and-system/airflow-docker-wsl-troubleshooting.md)
- [Deploying Airflow DAGs on EC2 (Docker)](dev-ops-and-system/2025-12-18-ec2-airflow-dag-deploy.md)

### Git & GitHub
- [GitHub video and media handling](git-and-github/github-video-and-media-handling.md)
- [Ubuntu WSL Essential Commands Cheat Sheet](git-and-github/ubuntu-wsl-git-cheat-sheet.md)
- [Pushing Only a Single File Using git stash](git-and-github/selective-file-commit-with-stash.md)
- [Rebase vs Merge Strategy](git-and-github/rebase-vs-merge-strategy.md)
- [GitHub Team Workflow Guide](git-and-github/github-team-workflow-guide.md)

### Linux
- [Linux Practical commands I used](linux/linux-operations-and-debugging.md)

### Python

- [dict.get() and unpacking patterns](python/dict-get-and-unpacking.md)
- [enumerate basics](python/enumerate-basics.md)
- [next() fundamentals](python/next-bascis.md)
- [Sorting dictionary by value and Top-N extraction](python/sorting-dict-by-value-and-top-n.md)

### Statistics

- [Mann-Whitney U Test practical notes](statistics/mann-whiteney-u-test.md)

---

## 💡 About

Each entry documents a real issue resolved, concept clarified, or system behavior understood through hands-on experience.

---

## 🧠 Patterns I’m Learning Repeatedly

- Idempotent pipeline design
- Separation of orchestration vs transformation (Airflow vs dbt)
- Observability via Slack alerts
- Debugging containerized environments
- Streaming window mechanics
- Git workflow discipline (rebase vs merge decisions)
